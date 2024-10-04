import speech_recognition as sr
import google.generativeai as genai
from  dotenv  import load_dotenv
from gtts import gTTS
import re 
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# To take voice input from the user 
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something:")
        audio = r.listen(source)
    try:
        text=r.recognize_google(audio)
        print("You said: ", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio")
    except sr.RequestError as e:
        print("Could not request result from google speech recognition service: {0}".format(e))


# Generating response from the llm 
def text_to_speech(text):
    tts=gTTS(text=text, lang="en")
    #save the speech from the given text in the mp3 format
    tts.save("speech.mp3")


def llm_model_object(user_text):
    # Configure the API with your Google API key
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Choose the model you want to use
    model = genai.GenerativeModel('gemini-pro')
    
    # Generate the content based on the user's text
    response = model.generate_content(user_text)
    
    # Extracting the text from the first candidate
    if hasattr(response, 'candidates') and len(response.candidates) > 0:
        candidate = response.candidates[0]
        if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
            if len(candidate.content.parts) > 0 and hasattr(candidate.content.parts[0], 'text'):
                result = candidate.content.parts[0].text  # Access the text
                result = re.sub(r"\*", "", result)
            else:
                result = "Sorry, I couldn't generate a proper response (no text found in parts)."
        else:
            result = "Sorry, I couldn't generate a proper response (no content found)."
    else:
        result = "Sorry, no candidates were returned."

    return result



