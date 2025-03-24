import json
import pandas as pd
import spacy
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

nlp = spacy.load("en_core_web_sm")

with open("data/human_language.json", "r", encoding="utf-8") as file:
    data = json.load(file)

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

with open("data/processed_human_language.json", "w", encoding="utf-8") as outfile:
    json.dump(df.to_dict(orient="records"), outfile, ensure_ascii=False, indent=4)

X_train, X_test, y_train, y_test = train_test_split(df['example'], df['intent'], test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = SVC(kernel='linear')
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)
print(f"Độ chính xác: {accuracy:.4f}")
print(classification_report(y_test, y_pred))
