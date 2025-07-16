import requests
import os

BASE_URL = "http://localhost:8000"

def test_health_check():
    response = requests.get(f"{BASE_URL}/document/health")
    print("Health Check Response:")
    print(response.json())

def test_parse_document(file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/document/parse", files=files)
    
    if response.status_code == 200:
        result = response.json()
        print("Parsed Entities:")
        for entity_type, entities in result["entities"].items():
            print(f"\n{entity_type.upper()}:")
            for entity in entities:
                print(f"- {entity['text']} (Confidence: {entity['confidence']:.2f})")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    test_health_check()
    print("\nTesting document parsing...")
    test_parse_document("data/raw/invoices/invoice_Roger Demir_17346-1.png")