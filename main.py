import argparse
from argparse import Namespace
import re
import torch
import json
import os
from utils import PROMPTS
import requests
from typing import Union
from slots import Ordering, ParingFood, AskInfo

def generate_response_Ollama(prompt, model="llama3.1:70b"):
    
    url = "http://10.234.0.160:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        text = response.json()
        return text.get("response", "")
        # return response.json().get("generated_text", "")
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return ""

def parsing_json(text):
    json_match = re.search(r"{.*}", text, re.DOTALL)

    if json_match:
        extracted_json = json_match.group()
        # Optionally format it without spaces or newlines
        compact_json = json.dumps(json.loads(extracted_json), separators=(',', ':'))
        # convert the json string to a dictionary
        compact_json = json.loads(compact_json)
        return compact_json

# class DMTracker:
#     def __init__(self):
#         self.possible_intent = ["risotto_ordering", "drink_ordering"]
#         self.intents = None
#         self.possible_slots = [RisottoSlots(), DrinkSlots()]
#         self.slots = None
    
#     def update(self, nlu_json):
#         # get the intent
#         if nlu_json["intent"] in self.possible_intent and nlu_json["intent"] not in self.intents:
#             self.intents.append( nlu_json["intent"] )
#             self.slots.append( self.possible_slots[self.intents.index(nlu_json["intent"])] )

#         # get the slots
#         for key, value in self.slots:
#             if key in self.slots.__dict__:
#                 self.slots.__dict__[key] = nlu_json["slots"][key]

class RisottoSlots:
    def __init__(self):
        self.slot = {
            "type": None,
            "cheese_on_top": None,
            "num_slice_meat": None,
            "size": None,
            "consistency": None
        }

        self.values = {
            "type": ["funghi", "speck", "milanese"],
            "cheese_on_top": ["grana", "parmigiano", "senza lattosio", "no"],
            "num_slice_meat": ["0", "1", "2", "3"],
            "size": ["baby", "normal", "big"],
            "consistency": ["creamy", "normal"]
        }

    def items(self):
        return self.slot.items()
    
class DrinkSlots:
    def __init__(self):
        self.type = None

class History():
    def __init__(self):
        self.messages = []
        self.intent = []
        self.roles = []

    def add_msg(self, msg, role, intent):
        self.roles.append(role)
        self.messages.append(msg)
        self.intent.append(intent)

    def clear(self):
        self.messages = []
        self.intent = []
    
    def get_history(self):
        return self.messages
    
    def intent_history(self):
        return ', \n'.join(self.intent)

    # def to_msg_history(self)->list[dict]:
    #     history = [{'role': role, 'content': msg} for role, msg in zip(self.roles, self.messages)]
    #     if len(history) > 5:
    #         return history[-5:]
        # return history

class DMTracker:
    def __init__(self):
        self.possible_intent = ['wine_ordering', 'paring_food', 'ask_info', 'out_of_domain']
        self.intentions = []
        self.ordering = None
        self.paring_food = None
        self.ask_info = None
    
    def update(self, input: dict):
        intent = input["intent"]

        if intent in self.possible_intent:
            if intent not in [x["intent"] for x in self.intentions]:
                self.intentions.append(intent)

                if 'ordering' in intent:
                    self.ordering = Ordering()
                elif 'paring_food' in intent:
                    self.paring_food = ParingFood()
                elif 'ask_info' in intent:
                    self.ask_info = AskInfo()
        
        #consider the slots of the intent = nlu_json["intent"]

        input = input["slots"] 

        for field in input:
            if input[field] != 'null':
                if 'ordering' in intent:
                    setattr(self.ordering, field, input[field])
                elif 'paring_food' in intent:
                    setattr(self.paring_food, field, input[field])
                elif 'asking_info' in intent:
                    setattr(self.ask_info, field, input[field])


        # slots = [x["slots"] for x in self.intentions if x["intent"] == input["intent"]][0]

        # for key, value in slots.items():
        #     if value == None and input["slots"][key] != 'null':
        #         slots.slot[key] = input["slots"][key]

        # # reassign the slots to the intent
        # for x in self.intentions:
        #     if x["intent"] == input["intent"]:
        #         x["slots"] = slots
    
    def dictionary(self, intent_ret):
        for x in self.intentions:
            if x == intent_ret:
                if 'ordering' in x:
                    dict_ret = {
                        "intent": x,
                        "slots": self.ordering
                    }
                elif 'paring_food' in x:
                    dict_ret = {
                        "intent": x,
                        "slots": self.paring_food
                    }
                elif 'asking_info' in x:
                    dict_ret = {
                        "intent": x,
                        "slots": self.ask_info
                    }
                return dict_ret

class NLU():
    def __init__(self):
        pass
    
    def __call__(self, user_input):
        nlu_text = PROMPTS["NLU"] + user_input
        nlu_output = generate_response_Ollama(nlu_text)
        nlu_output = nlu_output.strip()

        with open("nlu_output.txt", "w") as file:
            file.write(nlu_output)
        nlu_js = parsing_json(nlu_output)
        return nlu_js

class Dialogue:
    def __init__(self):
        self.nlu = NLU()
        self.dm = None
        self.nlg = None
        self.tracker = DMTracker()
        self.history = History()

    def start(self):
        starting = 'Hi, I am your wine assistant. How can I help you?'
        self.history.add_msg(starting, 'assistant', 'init')
        user_input = input(starting + '\n')
        self.history.add_msg(user_input, 'user', 'input')

        # exit the loop using CTRL+C
        while True:
            
            # get the NLU output
            infos = self.nlu(user_input)
            print(type(infos))
            print(f"NLU: {infos}")
            self.tracker.update(infos)
            print(f"Tracker: {self.tracker.intentions}")
            # #class DMTracker
            # dm_tracker.update(nlu_js)

            # nlu_output = dm_tracker.return_values(nlu_js["intent"])

            # # get the DM output
            # dm_text = PROMPTS["DM"] +'\n'+ nlu_output
            # dm_output = query_ollama(dm_text)
            # print(f"DM: {dm_output}")

            # # Optional Pre-Processing for NLG
            # dm_output = dm_output.strip()

            # # get the NLG output
            # nlg_text = PROMPTS["NLG"] + dm_output
            
            # nlg_output = query_ollama(nlg_text)

            # print(f"NLG: {nlg_output}")

def main():
    # args = get_args()
    dg = Dialogue()
    dg.start()

if __name__ == "__main__":
    main()
