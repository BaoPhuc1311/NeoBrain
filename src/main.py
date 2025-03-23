import json
import pandas as pd

with open("data/human_language.json", "r", encoding="utf-8") as file:
    data = json.load(file)

records = []
for category, details in data["categories"].items():
    for intent in details["intents"]:
        for example in intent["examples"]:
            records.append({
                "category": category,
                "intent": intent["name"],
                "description": intent["description"],
                "example": example
            })

df = pd.DataFrame(records)

print(df.head())
