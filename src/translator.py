from deep_translator import GoogleTranslator
 

def translator(text, target_lang="en"):
    translated = GoogleTranslator(source='auto', target=target_lang).translate(text)

    return translated


if __name__ == "__main__":
    input_text = input("enter your text : ")
    target_language = input("،translate to :(en, de, fr, fa): ")
    
    result = translator(input_text, target_language)
    print("Translated Text : ", result)