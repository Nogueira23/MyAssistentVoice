import speech_recognition as sr
from playsound import playsound
from requests import get
from bs4 import BeautifulSoup
from createAudio import ManegerAudio
import os
import webbrowser as browser
from win10toast import ToastNotifier
import json
import time


##### CONFIGURAÇÕES #####
assistentName = 'rose'
managerAudio = ManegerAudio()
toaster = ToastNotifier()

##### FUNÇÕES DE CÁLCULOS ####

def extracao_digitos(trigger):
    caracteres = []

    for aux in trigger:
        if aux.isdigit():
            caracteres.append(aux)
    
    string = ''.join(caracteres)

    return string

##### FUNÇÕES PRINCIPAIS ####
def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google(audio, language='pt-BR')
                trigger = trigger.lower()
                #print(trigger)
                #breakpoint()

                if assistentName in trigger:
                    print('Rose: ', trigger)
                    ### executar os comandos
                    #responde('feedback')
                    executa(trigger)

            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger

def responde(arquivo):
    playsound('audios/' + arquivo + '.mp3')

def executa(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()
    elif 'temperatura' in trigger:
        previsao_tempo(temp=True)
    elif 'tempo' in trigger:
        previsao_tempo(tempo=True)
    elif 'desliga o pc' or 'desliga o computador' in trigger:
        power_pc(poweroff=True)
    elif 'programa o pc para desligar' or 'programa o computador para desligar' in trigger :
        power_pc(program_poweroff=True)
    elif 'reinicia o pc' or 'reinicia o computador' in trigger:
        power_pc(reboot=True)
    elif 'suspende o pc' or 'suspende o computador' in trigger:
        power_pc(suspend=True)
    elif 'hiberna o pc' or 'hiberna o computador' in trigger:
        power_pc(hibernate=True)
    elif 'abrir playlist' or 'abre a playlist' in trigger:
        playlits()
    elif 'abre a netflix' or 'abrir netflix' in trigger:
        netflix()
    elif 'abre a hbo' or 'abrir hbo' in trigger:
        hbo()
    elif 'abre a star plus' or 'abrir star plus' in trigger:
        star_plus()
    else:
        responde('comando_invalido')

### FUNÇÕES DE COMANDO ###
def ultimas_noticias():
    site = get("https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419")
    news = BeautifulSoup(site.text, 'html.parser')
    for item in news.findAll('item')[:2]:
        mensage = item.title.text
        managerAudio.create_audio(mensage, 'noticias')
        managerAudio.play_audio('noticias')

def previsao_tempo(temp=False, tempo=False):
    site = get('https://api.openweathermap.org/data/2.5/weather?q=campinas,sao+paulo&lang=pt&appid=de0cdab7ef89e3f55d8a31c79ced20d7&units=metric')
    siteJson = site.json()
    temperatura = siteJson['main']['temp']
    temp_min = siteJson['main']['temp_min']
    temp_max = siteJson['main']['temp_max']
    tempo_describe = siteJson['weather'][0]['description']
    if temp:
        menssage = f'A temperatura é de {temperatura} graus'
        name = 'temperatura'
    if tempo:
        menssage = f'A previsão de hoje é que teremos uma temperatura máxima de {temp_max:,.0f} graus e uma mínima de {temp_min:,.0f} graus, com {tempo_describe}'
        name = 'tempo'
    managerAudio.create_audio(menssage, name)
    responde(name)

def power_pc(poweroff=False, reboot=False, suspend=False, hibernate=False, program_poweroff=False):
    if poweroff:
        menssage = f'O computador será desligado em 10 segundos'
        os.system('shutdown -s -t 10')
    if program_poweroff:
        responde('time_poweroff')
        trigger = managerAudio.start_micro()
        if 'hora' and 'uma' in trigger:
            menssage = f'O computador será desligado em uma hora'
            time_aux = 1
        if 'minutos' in trigger:
            time = int(extracao_digitos(trigger))
            time_aux = time*60
            menssage = f'O computador será desligado em {time} minutos'
        if ('hora' or 'horas') in trigger and 'uma' not in trigger:
            time = int(extracao_digitos(trigger))
            time_aux = time*60*60
            if time > 1:
                menssage = f'O computador será desligado em {time} horas'
            else:
                menssage = f'O computador será desligado em {time} hora'
        name = 'poweroff'
        os.system(f'shutdown -s -t {time_aux}')
    if reboot:
        menssage = f'O computador será reiniciado em 10 segundos'
        os.system('shutdown -r -t 10')
        name = 'reboot'
    if suspend:
        menssage = f'O computador será suspenso em 10s'
        os.system('powercfg -hibernate off')
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        name = 'suspend'
    if hibernate:
        menssage = f'O computador entrará em hibernação em 10 segundos'
        os.system('powercfg -hibernate on')
        os.system('rundll32.exe powrprof.dll,SetSuspendState Hibernate')
        name = 'hibernate'
    managerAudio.create_audio(menssage, name)
    managerAudio.play_audio(name)

def netflix():
    browser.open('https://www.netflix.com/browse')
    mensage = 'Pronto, bom filme e não esquece da pipoca'
    managerAudio.create_audio(mensage, 'netflix')
    managerAudio.play_audio('netflix')

def hbo():
    browser.open('https://play.hbomax.com/page/urn:hbo:page:home')
    mensage = 'Pronto, bom filme e não esquece da pipoca'
    managerAudio.create_audio(mensage, 'hbo')
    managerAudio.play_audio('hbo')

def star_plus():
    browser.open('https://starplus.com/')
    mensage = 'Pronto, bom filme e não esquece da pipoca'
    managerAudio.create_audio(mensage, 'starplus')
    managerAudio.play_audio('starplus')

def playlits():
    while True:
        responde('musica')
        trigger = managerAudio.start_micro()
        if 'tranquilo' in trigger:
            browser.open('https://open.spotify.com/playlist/37i9dQZF1E4BZxqDXbxJkg')
            responde('musica_tranquila')
            return False
        elif 'funk' in trigger:
            browser.open('https://open.spotify.com/playlist/62dVnvwA5eeHl9vZOrP6Mc')
            responde('funk')
            return False
        elif 'pagodinho' in trigger:
            browser.open("https://open.spotify.com/playlist/6CtOuhTeqIi66SYQkMmcSu")
            responde('pagode')
            return False
        else:
            responde('comando_invalido')
    

def main():
    monitora_audio()

main()
 