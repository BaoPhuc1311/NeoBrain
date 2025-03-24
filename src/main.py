import json
import pandas as pd
import re
import spacy
import os

nlp = spacy.load("en_core_web_sm")

try:
    with open("data/human_language.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Lỗi khi đọc file JSON: {e}")
    exit()

records = []
for category, details in data.get("categories", {}).items():
    category = category.strip().lower()
    for intent in details.get("intents", []):
        intent_name = intent["name"].strip().lower()
        description = intent["description"].strip()
        for example in intent.get("examples", []):
            example = example.strip().lower()
            doc = nlp(example)
            processed_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
            processed_text = " ".join(processed_tokens)
            records.append({
                "category": category,
                "intent": intent_name,
                "description": description,
                "example": processed_text
            })

df = pd.DataFrame(records)
df.drop_duplicates(subset=["category", "intent", "example"], inplace=True)

output_path = "data/processed_human_language.json"
with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(df.to_dict(orient="records"), outfile, ensure_ascii=False, indent=4)

print(f"Tổng số intent: {df['intent'].nunique()}")
print(f"Tổng số example: {len(df)}")
print(f"Các category: {df['category'].unique()}")
print(df.head())
