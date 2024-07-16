import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer 
import re
from textblob import TextBlob
from keybert import KeyBERT
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Optional
from googletrans import Translator
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

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
    clean: Optional[bool] = False

def translate_text_with_retry(text, src_lang, dest_lang):
    translator = Translator()
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            translation = translator.translate(text, src=src_lang, dest=dest_lang)
            return translation.text
        except Exception as e:
            print(f"Error en la traducción: {e}")
            retry_count += 1
            time.sleep(1)  # Espera antes de intentar nuevamente
    
    return None 

### API Análisis de sentimientos
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
        if data.clean:
            texto = clean_html(texto)
        #print(f"Texto procesado: {texto}")
        resultados_vader = sid.polarity_scores(texto)

        try:
            idioma = detect(texto)
            print(f"Idioma detectado: {idioma}")

            # Traducir al inglés si no está en inglés
            if idioma != 'en':
                traducido = translator.translate(texto, src=idioma, dest='en').text
            else:
                traducido = texto
        except LangDetectException as e:
            print(f"Error al detectar idioma: {e}")
            traducido = texto

        print(f"Texto traducido: {traducido}")

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

        frases_nominales = list(blob.noun_phrases)
        #print(f"Frases nominales: {frases_nominales}")

        p_clave = kw_model.extract_keywords(texto, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
        palabras_clave = [keyword for keyword, score in p_clave]
        #print(f"Palabras clave: {palabras_clave}")

        texto_tokenizado = WordPunctTokenizer().tokenize(texto)

        resultados["analisis_de_sentimientos"].append(resultados_vader)
        resultados["sentimientos_textblob"].append(resultados_textblob)
        resultados["frases_nominales"].append(frases_nominales)
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

from googletrans import Translator, LANGUAGES
import time

translator = Translator()

def translate_text_with_retry(text, src_lang, dest_lang):
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            translation = translator.translate(text, src=src_lang, dest=dest_lang)
            return translation.text
        except Exception as e:
            print(f"Error en la traducción: {e}")
            retry_count += 1
            time.sleep(1)  # Espera antes de intentar nuevamente
    
    return None  # Manejo de error más robusto según tus necesidades

# Ejemplo de uso
texto = "Hola, cómo estás?"
traducido = translate_text_with_retry(texto, src='es', dest='en')
if traducido:
    print(f"Texto traducido: {traducido}")
else:
    print("No se pudo traducir el texto.")


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