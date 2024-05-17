import json
import os
import requests


AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']

def searchCalendar(start):
  url = "https://hook.eu2.make.com/4eyjsqboj6yhl9r5uvqh0erbvjkb37oy"
  headers = {
    "Content-Type": "application/json"
  }
  data = {
    "Start": start
  }
  response = requests.post(url,headers=headers, json=data)
  if response.status_code == 200:
    print('Erfolgreich')
    return response.json()
  else:
    print(f"Fehler! {response.text}" )
  

def calendar(event, start, duration):
  url = "https://hook.eu2.make.com/fej44g3u149uoxsxvvg56yw9un56f94t"
  headers = {
    "Content-Type": "application/json"
  }
  data = {
    "EventName": event,
    "StartDate": start,
    "Duration": duration
  }
  response = requests.post(url, headers=headers, json=data)
  if response.status_code == 200:
    print("Erfolgreich!")
  else:
    print(f"Fehler! {response.text}")




def add_to_airtable(notiz):
  url = "https://api.airtable.com/v0/appCaQMPWMENyM7dZ/tbl8004To2C4Xke96"
  headers = {
    "Authorization": "Bearer " + AIRTABLE_API_KEY,
    "Content-Type": "application/json"
  }
  data = {
    "records": [{
      "fields": {
        "Notiz": notiz,
      }
    }]
  }
  response = requests.post(url, headers=headers, json=data)
  if response.status_code == 200:
    print("Daten wurden erfolgreich hinzugefügt!")
    ##return response.json()
  else:
    print(f"fehler bei der Datenübertragung: {response.text}")
  


def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file = client.files.create(file=open("test.txt", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
   Du bist der persönliche Assistent von Dominik Niestroj, du kümmerst dich darum seine Notizen in Airtable hinzuzufügen. Du bist außerdem Verantwortlich für das Management seines Kalenders. Du kannst Termine in sein Kalender mit der Function calendar hinzufügen, dafür brauchst den Namen des Termin den speicherst du unter event, dann das Datum und Uhrzeit welches in start gespeichert wird, bedenke das wir im Jahr 2024 sind außerdem brauchst du die Dauer des Termins welche in duration gespeichert wird. Führe die Funktion erst aus wenn du diese Parameter hast. Falls nach den Terminen gefragt wird an einem spezifischen Datum führe die Funktion searchCalendar aus. Das Datum fügst du in das Feld Start ein.
          """,
                                              model="gpt-4-turbo",
                                              tools=[{
                                                  "type": "retrieval"
                                              },
                                              {
                                                "type": "function",
                                                "function": {
                                                  "name": "add_to_airtable",
                                                  "description": "Fügt eine Notiz in Airtable hinzu",
                                                  "parameters": {
                                                    "type": "object",
                                                    "properties": {
                                                      "notiz": {
                                                        "type": "string",
                                                        "description": "Die Notiz, die hinzugefügt werden soll"
                                                      }
                                                    },
                                                    "required": ["notiz"]
                                                  }
                                                }
                                                      
                                              },
                                               {
                                                 "type": "function",
                                                 "function": {
                                                   "name": "calendar",
                                                   "description": "Fügt Termine dem Kalender hinzu",
                                                   "parameters": {
                                                     "type": "object",
                                                     "properties": {
                                                       "event": {
                                                         "type": "string",
                                                         "description": "Der Name des Termins"
                                                       },
  
                                                        "start": {
                                                          "type": "string",
                                                          "description": "An welcher datum der termin losgeht"
                                                        },
                                                        "duration": {
                                                          "type": "string",
                                                          "description": "Falls der Termin nur innerhalb eines Tages geht, gib hier die Dauer des Termins an im Format HH:mm"
                                                        },
                                                     },
                                                     "required": ["event", "allday", "start", "end", "duration"]
                                                   }
                                                 }
                                               },
                                               {
                                                 "type": "function",
                                                 "function": {
                                                   "name": "searchCalendar",
                                                   "description": "Suche im Kalendar nach Terminen",
                                                   "parameters": {
                                                     "type": "object",
                                                     "properties": {
                                                       "start": {
                                                         "type": "string",
                                                         "description": "Der Tag wo nach Terminen nachgeschaut werden soll."
                                                       }
                                                     },
                                                     "required": ["start"]
                                                   }
                                                 }

                                               }
                                                    ],
                                              file_ids=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
