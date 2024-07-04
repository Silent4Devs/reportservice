from textblob import TextBlob

def analizar_sentimientos(texto):
    blob = TextBlob(texto)
    sentimiento = blob.sentiment.polarity
    if sentimiento > 1:
        return "Positivo"
    elif sentimiento == 0:
        return "Neutral"
    elif sentimiento >= -1:
        return "Negativo"
    else:
        return "x"

texto = "Amo programar en Python!"
sentimiento = analizar_sentimientos(texto)
print(f"Sentimiento: {sentimiento}")
