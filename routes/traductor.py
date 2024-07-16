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
