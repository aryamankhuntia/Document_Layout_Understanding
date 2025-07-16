import os
import sys
import logging
import pytesseract
import numpy as np
import torch
from PIL import Image
from typing import Dict, List, Tuple, Any
from transformers import LayoutLMv3ForTokenClassification, LayoutLMv3Processor

logger = logging.getLogger(__name__)

class DocumentParser:
    def __init__(self, model_path: str):
        logger.info(f"Loading model from {model_path}")
        try:
            self.model = LayoutLMv3ForTokenClassification.from_pretrained(model_path)
            self.processor = LayoutLMv3Processor.from_pretrained(model_path, apply_ocr=False)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Using device: {self.device}")
            self.model.to(self.device)
            self.model.eval()
            self.id2label = self.model.config.id2label
            
            self.use_iob = any(label.startswith('B-') for label in self.id2label.values())
            logger.info(f"Model uses IOB tags: {self.use_iob}")
            
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def extract_text_blocks(self, image: Image.Image) -> List[Dict]:
        try:
            data = pytesseract.image_to_data(
                np.array(image),
                output_type=pytesseract.Output.DICT,
                config='--psm 6'
            )
            blocks = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 60 and data['text'][i].strip() != "":
                    block = {
                        'text': data['text'][i],
                        'bbox': [
                            int(data['left'][i]),
                            int(data['top'][i]),
                            int(data['left'][i] + data['width'][i]),
                            int(data['top'][i] + data['height'][i])
                        ],
                        'line_num': int(data['line_num'][i])
                    }
                    blocks.append(block)
            return blocks
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            raise

    def parse_document(self, image: Image.Image) -> Dict[str, Dict[str, List[Dict]]]:
        try:
            ocr_blocks = self.extract_text_blocks(image)
            if not ocr_blocks:
                logger.warning("No text blocks found in image")
                return {"entities": {}}
            
            words = [block['text'] for block in ocr_blocks]
            raw_boxes = [block['bbox'] for block in ocr_blocks]
            line_nums = [block['line_num'] for block in ocr_blocks]
            
            width, height = image.size
            normalized_boxes = []
            for box in raw_boxes:
                left, top, right, bottom = box
                normalized_boxes.append([
                    max(0, min(1000, int(left / width * 1000))),
                    max(0, min(1000, int(top / height * 1000))),
                    max(0, min(1000, int(right / width * 1000))),
                    max(0, min(1000, int(bottom / height * 1000)))
                ])
            
            encoding = self.processor(
                image,
                words,
                boxes=normalized_boxes,
                return_tensors="pt",
                return_offsets_mapping=True,
                padding="max_length",
                truncation=True,
                max_length=512
            )
            
            inputs = {k: v.to(self.device) for k, v in encoding.items() 
                      if k != "offset_mapping"}
            offset_mapping = encoding.get("offset_mapping")[0].cpu().numpy()
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            predictions = outputs.logits.argmax(-1).squeeze(0).cpu().numpy()
            word_predictions = []
            
            for word_idx in range(len(words)):
                if word_idx >= len(offset_mapping):
                    break
                    
                token_indices = encoding.word_to_tokens(word_idx)
                if token_indices is None:
                    continue
                    
                word_token_preds = predictions[token_indices.start:token_indices.end]
                
                if len(word_token_preds) == 0:
                    continue
                    
                unique, counts = np.unique(word_token_preds, return_counts=True)
                majority_label = unique[np.argmax(counts)]
                
                word_predictions.append({
                    'text': words[word_idx],
                    'bbox': raw_boxes[word_idx],
                    'label': self.id2label.get(int(majority_label), "O"),
                    'line_num': line_nums[word_idx]
                })
            
            entities = self._group_entities(word_predictions)
            return {"entities": entities}
            
        except Exception as e:
            logger.error(f"Document parsing failed: {str(e)}")
            return {"entities": {}}

    def _group_entities(self, word_predictions: List[Dict]) -> Dict[str, List[Dict]]:
        sorted_words = sorted(word_predictions, key=lambda w: (w['line_num'], w['bbox'][0]))
        entities = {}
        current_entity = None
        for word in sorted_words:
            label = word['label']
            
            if label == "O" or not word['text'].strip():
                if current_entity:
                    self._finalize_entity(entities, current_entity)
                    current_entity = None
                continue
                
            if self.use_iob:
                entity_type = label.replace("B-", "").replace("I-", "")
                is_begin = label.startswith("B-")
            else:
                entity_type = label
                is_begin = True
                
            should_start_new = (
                is_begin or 
                (current_entity and current_entity["type"] != entity_type) or
                (current_entity and not self._should_merge(current_entity, word))
            )
            
            if should_start_new:
                if current_entity:
                    self._finalize_entity(entities, current_entity)
                
                current_entity = {
                    "type": entity_type,
                    "text": word['text'],
                    "bbox": word['bbox'],
                    "line_num": word['line_num']
                }
            else:
                current_entity["text"] += " " + word['text']
                current_entity["bbox"] = [
                    min(current_entity["bbox"][0], word['bbox'][0]),
                    min(current_entity["bbox"][1], word['bbox'][1]),
                    max(current_entity["bbox"][2], word['bbox'][2]),
                    max(current_entity["bbox"][3], word['bbox'][3])
                ]
                current_entity["line_num"] = word['line_num']

        if current_entity:
            self._finalize_entity(entities, current_entity)
        
        return entities

    def _should_merge(self, current_entity: Dict, next_word: Dict) -> bool:
        if current_entity["line_num"] == next_word['line_num']:
            return True
            
        current_bbox = current_entity["bbox"]
        next_bbox = next_word['bbox']
        vertical_gap = next_bbox[1] - current_bbox[3]
        
        line_height = current_bbox[3] - current_bbox[1]
        return vertical_gap < line_height * 1.5

    def _finalize_entity(self, entities: Dict, entity: Dict) -> None:
        entity_data = {
            "text": entity["text"],
            "bbox": entity["bbox"],
            "confidence": 1.0
        }
        entities.setdefault(entity["type"], []).append(entity_data)