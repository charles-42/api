from fastapi import FastAPI
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

"""
{
        "name": "api",
        "runtime": "python3.7",
        "endpoint": "https://knd7yw.deta.dev",
        "visor": "enabled",
        "http_auth": "disabled"
}
"""
app = FastAPI()


@app.get("/")
def read_root():
    tfidf, model = pickle.load(open('model.bin', 'rb'))
    lol = pickle.load(open('lol', 'rb'))
    # print('model loaded!')
    input = "i'm sad"
    predictions = model.predict(tfidf.transform([input]))
    label = predictions[0]
    return('{} : {}'.format(input, label))
    # return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}