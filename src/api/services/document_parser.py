import torch
import numpy as np
import pytesseract
from PIL import Image
from transformers import LayoutLMv3ForTokenClassification, LayoutLMv3Processor
from typing import Dict, List, Tuple

class DocumentParser:
    def __init__(self, model_path: str):
        self.model = LayoutLMv3ForTokenClassification.from_pretrained(model_path)
        self.processor = LayoutLMv3Processor.from_pretrained(model_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    def extract_text_blocks(self, image: Image.Image) -> List[Dict]:
        data = pytesseract.image_to_data(
            np.array(image),
            output_type=pytesseract.Output.DICT,
            config='--psm 11'
        )

        blocks=[]
        for i in range(len(data['text'])):
            if int(data['conf'][i])>60 and data['text'][i].strip()!="":
                block={
                    'text':data['text'][i],
                    'bbox':[
                        data['left'][i],
                        data['right'][i],
                        data['left'][i] + data['width'][i],
                        data['top'][i] + data['height'][i]
                    ]
                }
                blocks.append(block)
        return blocks
    
    def parse_document(self, image: Image.Image) -> Dict[str, List[Dict]]:
        ocr_blocks=self.extract_text_blocks(image)
        words = [block['text'] for block in ocr_blocks]
        raw_boxes = [block['bbox'] for block in ocr_blocks]

        width, height = image.size
        normalized_boxes=[]
        for box in raw_boxes:
            left, top, right, bottom = box
            normalized_box=[
                max(0, min(1000, int(left/width*1000))),
                max(0, min(1000, int(top/height*1000))),
                max(0, min(1000, int(right/width*1000))),
                max(0, min(1000, int(bottom/height*1000)))
            ]
            normalized_boxes.append(normalized_box)

        encoding = self.processor(
            image,
            words,
            boxes=normalized_boxes,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=512
        )

        inputs={k: v.to(self.device) for k,v in encoding.items()}

        with torch.no_grad():
            outputs=self.model(**inputs)

        predictions = outputs.logits.argmax(-1).squeeze().tolist()

        entities = self._group_entities(words, raw_boxes, predictions)

        return entities
    
    def _group_entities(self, words: List[str], boxes: List[List[int]], predictions: List[int]) -> Dict[str, List[Dict]]:
        current_entity=None
        entities={}
        id2label=self.model.config.id2label

        for word, box, pred_idx in zip(words, boxes, predictions):
            label = id2label[pred_idx]
            if label=="other" or label=="O" or not word.strip():
                continue
            entity_type=label.replace("B-","").replace("I-","")
            if not current_entity or current_entity["type"]!=entity_type:
                if current_entity:
                    entities.setdefault(current_entity["type"],[]).append(current_entity)
                current_entity={
                    "type":entity_type,
                    "test": word,
                    "bbox":box,
                    "confidence":1.0
                }

            else:
                current_entity["text"] += " " + word
                current_entity["bbox"] = [
                    min(current_entity["bbox"][0], box[0]),
                    min(current_entity["bbox"][1], box[1]),
                    max(current_entity["bbox"][2], box[2]),
                    max(current_entity["bbox"][3], box[3])
                ]
        if current_entity:
            entities.setdefault(current_entity["type"], []).append(current_entity)

        return entities