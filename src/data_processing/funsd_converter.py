import os
import json
from collections import defaultdict

def convert_funsd_to_layoutlm(input_dir, output_dir):
    """Convert FUNSD annotations to LayoutLM format"""
    os.makedirs(output_dir, exist_ok=True)
    
    for split in ['training', 'testing']:
        image_dir = os.path.join(input_dir, f"{split}_data", "images")
        ann_dir = os.path.join(input_dir, f"{split}_data", "annotations")
        
        output_data = []
        for ann_file in os.listdir(ann_dir):
            if not ann_file.endswith('.json'):
                continue
                
            with open(os.path.join(ann_dir, ann_file), 'r') as f:
                data = json.load(f)
                
            image_path = os.path.join(image_dir, ann_file.replace('.json', '.png'))
            words = []
            bboxes = []
            labels = []
            
            for element in data['form']:
                for word in element['words']:
                    words.append(word['text'])
                    bboxes.append(word['box'])  # [x1, y1, x2, y2]
                    labels.append(element['label'])
            
            output_data.append({
                "id": ann_file.replace('.json', ''),
                "words": words,
                "bboxes": bboxes,
                "labels": labels,
                "image_path": image_path
            })
        
        # Save converted data
        output_path = os.path.join(output_dir, f"{split}.json")
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
            
        print(f"Converted {len(output_data)} {split} documents")

# Example usage
if __name__ == "__main__":
    funsd_path = "../../data/raw/FUNSD/dataset"
    output_path = "../../data/processed/FUNSD"
    convert_funsd_to_layoutlm(funsd_path, output_path)