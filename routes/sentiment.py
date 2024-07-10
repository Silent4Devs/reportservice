import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer 
import re
from sklearn.metrics import f1_score

#### Def de limpieza de textos
def clean_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s.,?!]', '', text)
    return text

####Tokenizado

texto = "¿Cuánto tiempo pasó desde que comí una manzana?"
texto_tokenizado = WordPunctTokenizer().tokenize(texto)
print(texto_tokenizado)

#### Semáforo
a = "I do not like talk with my mom"
y = "I like eat pozole with my family"
z = "My notebook is black"

sid=SentimentIntensityAnalyzer()
resultados=sid.polarity_scores(z)

resultados_json = json.dumps(resultados)
print(resultados_json)

#### Precision F1-score
true_labels = [0, 1, 0, 1, 0, 1, 1]  
predicted_labels = [0, 0, 0, 1, 0, 1, 1]  

f1 = f1_score(true_labels, predicted_labels)
print(f'F1-Score: {f1}')



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


import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import spacy

# Descargar los recursos necesarios
nltk.download('vader_lexicon')
spacy.cli.download("en_core_web_sm")

# Inicializar los analizadores
sid = SentimentIntensityAnalyzer()
nlp = spacy.load("en_core_web_sm")

# Texto de ejemplo
z = "My notebook is black"

# Análisis de sentimientos con VADER
resultados_vader = sid.polarity_scores(z)

# Análisis de subjetividad y polaridad con TextBlob
blob = TextBlob(z)
resultados_textblob = {
    "polarity": blob.sentiment.polarity,
    "subjectivity": blob.sentiment.subjectivity
}

# Extracción de frases nominales con TextBlob
frases_nominales = blob.noun_phrases

# Extracción de palabras clave importantes con spaCy
doc = nlp(z)
palabras_clave = [chunk.text for chunk in doc.noun_chunks]

# Compilar resultados
resultados = {
    "sentimientos_vader": resultados_vader,
    "sentimientos_textblob": resultados_textblob,
    "frases_nominales": list(frases_nominales),
    "palabras_clave": palabras_clave
}

# Convertir a JSON y mostrar
resultados_json = json.dumps(resultados, indent=4)
print(resultados_json)

