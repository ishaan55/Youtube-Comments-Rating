from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import json
import re
import nltk
import numpy as np
nltk.download('stopwords')
from nltk.corpus import stopwords
sw = stopwords.words('english')
sw.remove('not')
import pandas as pd
from yt import get_video_comments

# VIDEO_ID = 'lVbElR_HwXQ'
model = load_model('sentiment_analysis.keras')
print('Model Loaded')

def clean_texts(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    text = re.sub(r'(@[A-Za-z0-9_]+)|[^\w\s]|#|http\S+', '', text)
    text = emoji_pattern.sub(r'', text)
    text = " ".join([word for word in text.split() if word not in sw])
    text = text.lower()
    return text

def get_rating(VIDEO_ID):
    with open('tokenizer.json') as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)
        print(len(tokenizer.word_index))
        comments = pd.DataFrame(get_video_comments(VIDEO_ID), columns=['Comments'])
        print("Comments fetched")
        comments['Comments'] = comments['Comments'].apply(clean_texts)
        X_input = tokenizer.texts_to_sequences(comments['Comments'])
        X_input = pad_sequences(X_input, maxlen=100, padding = 'post')
        pred = (model.predict(X_input) >= 0.5).astype(int)
        return np.average(pred)
        