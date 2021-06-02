# import spacy
# from spacytextblob.spacytextblob import SpacyTextBlob
# from fastapi import FastAPI
# import pickle
# spacy.load('en_core_web_sm')


# app = FastAPI()

# def fonction_nlp():
#     nlp = spacy.load('en_core_web_sm')
#     text = 'Today is an amazing day!'
#     spacy_text_blob = SpacyTextBlob("Text", text)
#     nlp.add_pipe('spacytextblob')
#     pickle.dump(nlp, open('nlp.bin', 'wb'))
#     doc = nlp("happy")

#     return {'Polarity:': round(doc._.polarity, 2), 'Subjectivity:': round(doc._.subjectivity, 2)}


# print(fonction_nlp())
# # @app.get("/{user_input}")
# # async def root(user_input):
# #     return fonction_nlp(user_input)