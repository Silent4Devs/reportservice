import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer 
import re
from sklearn.metrics import f1_score
from textblob import TextBlob
from keybert import KeyBERT
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Optional

sentiment=APIRouter()

#### Def de limpieza de textos
def clean_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s.,?!]', '', text)
    return text

nltk.download('vader_lexicon')

class TextData(BaseModel):
    texts: List[str]

@sentiment.post('/sentimentAnalysis/', tags=["SentimentAnalysis"])
def sentiment_analysis(data: TextData):
    sid = SentimentIntensityAnalyzer()
    kw_model = KeyBERT()

    resultados = {
        "analisis_de_sentimientos": [],
        "sentimientos_textblob": [],
        "frases_nominales": [],
        "palabras_clave": []
        #"texto_tokenizado": []
    }

    for texto in data.texts:
        resultados_vader = sid.polarity_scores(texto)

        # Análisis de subjetividad (0 a 1) y polaridad (-1 a 1) con TextBlob
        blob = TextBlob(texto)
        resultados_textblob = {
            "polarity": blob.sentiment.polarity,
            "subjectivity": blob.sentiment.subjectivity
        }
        # Un valor más cercano a 1 indica que el texto es subjetivo, 
        # es decir, refleja opiniones, sentimientos o creencias personales. 
        # Un valor más cercano a 0 indica que el texto es objetivo, 
        # es decir, presenta hechos y datos.

        frases_nominales = blob.noun_phrases
        p_clave = kw_model.extract_keywords(texto, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
        palabras_clave = [keyword for keyword, score in p_clave]
        texto_tokenizado = WordPunctTokenizer().tokenize(texto)

        resultados["analisis_de_sentimientos"].append(resultados_vader)
        resultados["sentimientos_textblob"].append(resultados_textblob)
        resultados["frases_nominales"].append(list(frases_nominales))
        resultados["palabras_clave"].append(palabras_clave)
        #resultados["texto_tokenizado"].append(texto_tokenizado)
    return resultados

    # resultados_json = json.dumps(resultados, indent=5)
    # print(resultados_json)

# # Ejemplo de uso
# x = "I do not like talk with my mom, because we always fight"
# y = "I like eat pozole with my family, all the food is delicious"
# z = "My notebook is black. It has a powerful processor and a lot of RAM."

# sentiment_analysis(x, y, z)



####Tokenizado
# texto = "¿Cuánto tiempo pasó desde que comí una manzana?"
# texto_tokenizado = WordPunctTokenizer().tokenize(texto)
# print(texto_tokenizado)

# #### Semáforo
# x = "I do not like talk with my mom"
# y = "I like eat pozole with my family"
# z = "My notebook is black"

# sid=SentimentIntensityAnalyzer()
# resultados_s=sid.polarity_scores(z)

# resultados_json = json.dumps(resultados_s)
# print(resultados_json)

#### Precision F1-score
# true_labels = [0, 1, 0, 1, 0, 1, 1]  
# predicted_labels = [0, 0, 0, 1, 0, 1, 1]  

# f1 = f1_score(true_labels, predicted_labels)
# print(f'F1-Score: {f1}')



# Ejemplo de uso
# html_content = """
# <html>
# <head><title>Ejemplo</title></head>
# <body>
# <h1>Hola, mundo!</h1>
# <p>Este es un ejemplo de <a href="http://example.com">página web</a> con HTML.</p>
# <p>¡Aquí hay más texto! 😊</p>
# </body>
# </html>
# """

# clean_text = clean_html(html_content)
# print(clean_text)