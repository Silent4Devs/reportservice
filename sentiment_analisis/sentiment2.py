from nltk.sentiment.vader import SentimentIntensityAnalyzer

x = "No me gusta caminar por el bosque en las mañanas"
y = "Me gusta comer pozole con mi familia"
z = "Comunmente platico con la gente en mi camino"

sid=SentimentIntensityAnalyzer()
resultados=sid.polarity_scores(x)

print(resultados)