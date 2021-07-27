import requests
import json
import pyttsx3
import speech_recognition as sr
import re

API_KEY="tQd6TYyFSTJF"
PROJECT_TOKEN="t4LMWUG1gwiE"
RUN_TOKEN="ttJTV8KgkexR"


class Data:
   def __init__(self,api_key,project_token):
      self.api_key=api_key
      self.project_token=project_token
      self.params={
         "api_key":self.api_key
      }
      self.get_data()
      
   def get_data(self):
      response=requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',params=self.params)
      self.data=json.loads(response.text)
      #print(self.data)
   
   def get_total_cases(self):
      data = self.data['total']
      for content in data:
         if content['name']=='Coronavirus Cases:':
            return content['value']
      return "0"
      
   def get_total_deaths(self):
      data = self.data['total']
      for content in data:
         if content['name']=='Deaths:':
            return content['value']
      return "0"
         
   def get_country_data(self,Country):
      data=self.data['country']
      for content in data:
         if content['name'].lower()==Country.lower():
            return content
      return "0"
      
   def get_list_countries(self):
      countries=[]
      for country in self.data['country']:
         countries.append(country['name']) 
      return countries 
       
         

def speak(text):
   engine=pyttsx3.init()
   engine.say(text)
   engine.runAndWait()
   


def get_audio():
   r=sr.Recognizer()
   with sr.Microphone() as source:
      audio=r.listen(source)
      said=""
      try:
         said = r.recognize_google(audio)
      except Exception as e:
         print("Exception:", str(e))
   return said.lower()

def main():
   print("Started Program")
   data=Data(API_KEY,PROJECT_TOKEN)
   #get_data()
   END_PHRASE="stop"
   country_list=data.get_list_countries()
   
   TOTAL_PATTERNS={
                  re.compile("[\w\s]+total [\w\s]+ cases"):data.get_total_cases,
                  re.compile("[\w\s]+total cases"):data.get_total_cases,
                  re.compile("[\w\s]+total [\w\s]+ deaths"):data.get_total_deaths,
                  re.compile("[\w\s]+total deaths"):data.get_total_deaths
                  }
       
   COUNTRY_PATTERNS={
                   re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
                   re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
                   }
                   
                    
   while True:
      print("Listening....")
      text=get_audio()
      print(text)
      result=None
      
      for pattern,func in COUNTRY_PATTERNS.items():
         if pattern.match(text):
            words=set(text.split(" "))
            for country in country_list:
               if country.lower() in words:
                  result=func(country)
                  break
            
      for pattern,func in TOTAL_PATTERNS.items():
         if pattern.match(text):
            result=func()
            break
      if(result):
         print(result)
         speak(result)         
      
      
      if text.find(END_PHRASE)!= -1:
         print("Exit")
         break

main()      
