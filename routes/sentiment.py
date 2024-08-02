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
import spacy
import gensim
from gensim import *
from transformers import pipeline
from langdetect import detect
from deep_translator import GoogleTranslator


sentiment=APIRouter()

#tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
#model = DistilBertModel.from_pretrained('distilbert-base-uncased')
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

#### Def de limpieza de textos
def clean_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s.,?!]', '', text)
    return text

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

nlp = spacy.load('en_core_web_lg')
class TextData(BaseModel):
    texts: List[str]
    clean: Optional[bool] = False

def get_noun_phrases(text):
    words = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(words)
    grammar = """
        NP: {<DT>?<JJ>*<NN.*>+}   # Determiner + Adjective(s) + Noun(s)
            {<NN.*>+}             # Noun(s)
            {<JJ>*<NN.*>+}        # Adjective(s) + Noun(s)
    """
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(tagged)
    
    phrases = []
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            phrase = ' '.join(word for word, tag in subtree.leaves())
            phrases.append(phrase)
    return phrases

def get_noun_phrases_spacy(text):
    doc = nlp(text)
    phrases = [chunk.text for chunk in doc.noun_chunks]
    return phrases

def bart_summary(text, max_length=100):
    # Asegúrate de que el texto no sea demasiado corto para el modelo de resumen
    if len(text) < 30:
        return text

    # Ajuste de los parámetros del resumen
    summary = summarizer(text, max_length=max_length, min_length=20, do_sample=False)
    return summary[0]['summary_text']


def translate_text(text, target_language='es'):
    detected_language = detect(text)
    if detected_language != target_language:
        translated = GoogleTranslator(source=detected_language, target=target_language).translate(text)
        return translated
    return text

### API Análisis de sentimientos
@sentiment.post('/sentimentAnalysis/', tags=["SentimentAnalysis"])
def sentiment_analysis(data: TextData):
    sid = SentimentIntensityAnalyzer()
    kw_model = KeyBERT()

    resultados = {
        "analisis_de_sentimientos": [],
        "sentimientos_textblob": [],
        "frases_nominales_spacy": [],
        "palabras_clave": [],
        "resumen_bart": []
    }

    for texto in data.texts:
        if data.clean:
            texto = clean_html(texto)
        #print(f"Texto procesado: {texto}")
        texto_es = translate_text(texto, target_language='es')
        resultados_vader = sid.polarity_scores(texto_es)

        # Análisis de subjetividad (0 a 1) y polaridad (0 a 1) con TextBlob
        blob = TextBlob(texto_es)
        resultados_textblob = {
            "polarity": blob.sentiment.polarity,
            "subjectivity": blob.sentiment.subjectivity
        }
        # Un valor más cercano a 1 indica que el texto es subjetivo, 
        # es decir, refleja opiniones, sentimientos o creencias personales. 
        # Un valor más cercano a 0 indica que el texto es objetivo, 
        # es decir, presenta hechos y datos.

        frases_nominales_spacy = get_noun_phrases_spacy(texto_es)

        p_clave = kw_model.extract_keywords(texto, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
        palabras_clave = [keyword for keyword, score in p_clave]
        #print(f"Palabras clave: {palabras_clave}")

        texto_en = translate_text(texto_es, target_language='en')
        resumen_en = bart_summary(texto_en)

        resumen_bart = translate_text(resumen_en, target_language='es')

        resultados["analisis_de_sentimientos"].append(resultados_vader)
        resultados["sentimientos_textblob"].append(resultados_textblob)
        resultados["frases_nominales_spacy"].append(frases_nominales_spacy)
        resultados["palabras_clave"].append(palabras_clave)
        resultados["resumen_bart"].append(resumen_bart)
    return resultados

#### Para probar:
#### {
#     "texts": ["En sesión presencial con el coordinador para revisar el correcto funcionamiento de su módulo y con ello liberar el módulo, salen nuevamente errores y se identifican correcciones solicitadas con anterioridad que no fueron aplicadas por el equipo de desarrollo. Es importante comentar que la parte de desarrollo la tenemos con el proveedor Evoluta; sin embargo por parte de Silent tenemos la tarea de validar el correcto funcionamiento en conjunto con el proveedor previo a la sesión con el cliente."]
# }


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