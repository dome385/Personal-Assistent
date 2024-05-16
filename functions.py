import json
import os
import requests


AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']


def add_to_airtable(data):
  url = "https://api.airtable.com/v0/appJQVY7qQxuXeWw"
  headers = {
    "Authorization": AIRTABLE_API_KEY,
    "Content-Type": "application/json"
  }
  data = {
    "records": [{
      "fields": {
        "Name": data["name"],
        "Email": data["email"],
        "Message": data["message"]
      }
    }]
  }
  response = requests.post(url, headers=headers, json=data)
  if response.status_code == 200:
    print("Daten wurden erfolgreich hinzugefügt!")
    return response.json()
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
   Du bist der persönöiche Assistent von Dominik Niestroj, du kümmerst dich darum seine Notizen in Airtable hinzuzufügen, seine Termine zu überwachen und zu überarbeiten.
          """,
                                              model="gpt-4-turbo",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file_ids=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
