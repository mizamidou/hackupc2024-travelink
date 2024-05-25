import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def load_data(filepath):
    return pd.read_csv(filepath)

tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

def get_sentiment(tweet):
    inputs = tokenizer(tweet, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    probs = softmax(outputs.logits.detach().numpy()[0])
    return dict(zip(['negative', 'neutral', 'positive'], probs))

def tweet_mentions_interests(tweet, interests):
    tweet_lower = tweet.lower()
    return any(keyword.lower() in tweet_lower for keywords in interests.values() for keyword in keywords)

def process_data(df, interests):
    df['mentions_interest'] = df['tweet'].apply(lambda x: tweet_mentions_interests(x, interests))
    filtered_df = df[df['mentions_interest']].copy()
    filtered_df['sentiment'] = filtered_df['tweet'].apply(get_sentiment)
    return filtered_df

def extract_sentiment_scores(df):
    for sentiment in ['negative', 'neutral', 'positive']:
        df[sentiment] = df['sentiment'].apply(lambda x: x[sentiment])
    return df

def normalize_data(df):
    scaler = StandardScaler()
    df[['negative', 'neutral', 'positive']] = scaler.fit_transform(df[['negative', 'neutral', 'positive']])
    return df

def cluster_data(df, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10).fit(df[['negative', 'neutral', 'positive']])
    df['cluster'] = kmeans.predict(df[['negative', 'neutral', 'positive']])
    return df, kmeans

def get_names_by_cluster(df):
    grouped = df.groupby('cluster')['Traveller Name']
    return grouped

def main(df):
    interests = {
        "gardening": ["gardening", "planting", "landscaping"],
        "cuisine": ["cuisine", "cooking", "culinary arts", "gastronomy"],
        "museums": ["museums", "exhibitions", "art galleries", "cultural centres"],
        "walking": ["walking", "strolling", "treading"],
        "parks": ["parks", "public gardens", "recreational areas"],
        "hiking": ["hiking", "trekking", "trail hiking"],
        "outdoors": ["park", "garden", "trail", "hiking", "walking", "strolling", "trekking", "outdoor", "nature"],
        "leisure": ["museum", "theatre", "cinema", "concert", "gallery", "exhibit", "show", "event"],
        "sports": ["sports", "soccer", "tennis", "basketball", "football", "baseball", "golf", "fitness", "gym"],
        "travel": ["travel", "vacation", "trip", "expedition", "cruise", "tour", "journey"],
        "food": ["cuisine", "cooking", "eating", "dining", "foodie", "gastronomy", "culinary"]
    }
    
    processed_df = process_data(df, interests)
    processed_df = extract_sentiment_scores(processed_df)
    processed_df = normalize_data(processed_df)
    clustered_df, kmeans_model = cluster_data(processed_df, 5)  
    grouped_names = get_names_by_cluster(clustered_df)

    return grouped_names