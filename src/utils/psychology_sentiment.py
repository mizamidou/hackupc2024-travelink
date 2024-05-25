import torch
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('Minej/bert-base-personality')
model = AutoModelForSequenceClassification.from_pretrained('Minej/bert-base-personality')

def predict_personality(texts, batch_size=128):
    labels = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1).tolist()
        batch_results = [{label: prob for label, prob in zip(labels, probs)} for probs in probabilities]
        results.extend(batch_results)
    return results

def extract_features(df):
    features = predict_personality(df['tweet'].tolist())
    return pd.DataFrame(features, columns=["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"])

def perform_clustering(df, n_clusters=5):
    features = extract_features(df)
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(features_scaled)
    return kmeans.labels_

# Load data
def main(df):
    df['cluster'] = perform_clustering(df)
    grouped = df.groupby('cluster')
    return grouped