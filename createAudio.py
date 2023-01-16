from gtts import gTTS
from playsound import playsound
import speech_recognition as sr


class ManegerAudio():    
    def create_audio(self, audio, name):
        tts = gTTS(audio, lang='pt-br')
        tts.save(f'audios/{name}.mp3')

    def play_audio(self, name):
        playsound('audios/feedback.mp3')
        playsound(f'audios/{name}.mp3')

    def start_micro(self):
        micro = sr.Recognizer()
        with sr.Microphone() as source:
            while True:
                print('Aguardando comando: ')
                audio = micro.listen(source)
                try:
                    trigger = micro.recognize_google(audio, language='pt-BR')
                    trigger = trigger.lower()
                    print('Rose: ', trigger)
                    return trigger

                except sr.UnknownValueError:
                    print("Audio não reconhecido")
                except sr.RequestError as e:
                    print("Erro de requisição; {0}".format(e))
