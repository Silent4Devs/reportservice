# from googletrans import Translator, LANGUAGES

# def detect_language(text):
#     translator = Translator()
#     try:
#         detection = translator.detect(text)
#         return detection.lang, detection.confidence
#     except Exception as e:
#         print(f"Error detecting language: {e}")
#         return None, None

# text = '이 문장은 한글로 쓰여졌습니다.'
# language, confidence = detect_language(text)
# if language:
#     print(f"The detected language is {LANGUAGES[language]} with confidence {confidence}")
# else:
#     print("Could not detect language")
