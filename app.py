from fastapi import FastAPI
import pickle

# from sklearn.feature_extraction.text import TfidfVectorizer

"""
heroku url : https://lit-spire-48980.herokuapp.com/
"""
app = FastAPI()


@app.get("/{input}")
def predict(input: str):
    tfidf, model = pickle.load(open('model.bin', 'rb'))
    predictions = model.predict(tfidf.transform([input]))
    label = predictions[0]
    return('{} : {}'.format(input, label))