import argparse
from argparse import Namespace
import re
import torch
import json
import os
import logging
from utils import PROMPTS
import requests
from typing import Union
from slots import Ordering, ParingFood, AskInfo, assign_field

logger = logging.getLogger('Dialogue')
logger.setLevel(logging.DEBUG)

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

def extract_action_and_argument(input_string):
    ## TODO add check in case there is more in the output string from the LLM
    # Remove any ' characters from the input string
    input_string = input_string.replace("'", "")
    input_string = input_string.replace("\"", "")
    # Define the regex pattern for extracting action and argument
    pattern = r'(\w+)\(([\w\s=]+)\)' #r'(\w+)\((.*)\)\s*=\s*(.*)' #r'(\w+)\((\w+)\)'
    match = re.match(pattern, input_string)
    
    if match:
        action = match.group(1)  # Extract the action
        argument = match.group(2)  # Extract the argument
        if '=' in argument:
            argument = argument.split('=')[1]
        return action, argument

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

    def to_msg_history(self)->list[dict]:
        history = [{'role': role, 'content': msg} for role, msg in zip(self.roles, self.messages)]
        if len(history) > 5:
            return history[-5:]
        return history

class DMTracker:
    def __init__(self):
        self.possible_intent = ['wine_ordering', 'paring_food', 'asking_info', 'out_of_domain']
        self.intentions = []
        self.ordering = None
        self.paring_food = None
        self.asking_info = None
    
    def update(self, input: dict):
        intent = input["intent"]

        if intent in self.possible_intent:
            if intent not in [x for x in self.intentions]:
                self.intentions.append(intent)

                if 'ordering' in intent:
                    self.ordering = Ordering()
                elif 'paring_food' in intent:
                    self.paring_food = ParingFood()
                elif 'asking_info' in intent:
                    self.asking_info = AskInfo()
        
        #consider the slots of the intent = nlu_json["intent"]

        input = input["slots"] 
        for field in input:
            if input[field] != 'null' and input[field] != None and input[field] != 'None':
                # print(f"Field: {field}")
                if 'ordering' in intent:
                    assign_field(self.ordering, field, input[field])
                elif 'paring_food' in intent:
                    assign_field(self.paring_food, field, input[field])
                elif 'asking_info' in intent:
                    assign_field(self.asking_info, field, input[field])

        return intent
    
    def dictionary(self, intent_ret):
        for x in self.intentions:
            if x == intent_ret:
                if 'ordering' in x:
                    dict_ret = {
                        "intent": x,
                        "slots": self.ordering.extract()
                    }
                elif 'paring_food' in x:
                    dict_ret = {
                        "intent": x,
                        "slots": self.paring_food.extract()
                    }
                elif 'asking_info' in x:
                    dict_ret = {
                        "intent": x,
                        "slots": self.asking_info.extract()
                    }
                print(f"Dict: {dict_ret}")
                return dict_ret

class Analizer():
    # used for pre-processing the input text - find all the intent possible in the text
    def __init__(self, history):
        self.history = history
        pass
    
    def __call__(self, text):
        # extract all the intent in the text
        # last_int = self.history.to_msg_history()
        # last_int = last_int[-5:] if (len(last_int) > 5) else last_int
        # last_int = "\n".join([f"{k['role']}: {k['content']}"  for k in last_int])
        # logger.info(f"History: {last_int}")
        
        nlu_text = PROMPTS["PRE-NLU"] + '\n' + text

        intents = generate_response_Ollama(nlu_text)
        print(f"Intents: {intents}")
        

class NLU():
    def __init__(self, history):
        self.history = history
        self.analizer = Analizer(history)
        pass
    
    def __call__(self, user_input):
        list_intents = self.analizer(user_input) #TODO 

        match list_intents[0]:
            case "wine_ordering":
                prompt = PROMPTS["Infos"]
            case "paring_food":
                prompt = PROMPTS["Food"]
            case "asking_info":
                prompt = PROMPTS["Order"]
        
        prompt = prompt + '\n' + PROMPTS["NLU"]

        last_int = self.history.to_msg_history()
        last_int = last_int[-5:] if (len(last_int) > 5) else last_int
        last_int = "\n".join([f"{k['role']}: {k['content']}"  for k in last_int])
        logger.info(f"History: {last_int}")

        nlu_text = prompt + '\n' + last_int + '\n' + user_input

        nlu_output = generate_response_Ollama(nlu_text)
        nlu_output = nlu_output.strip()

        with open("nlu_output.txt", "w") as file:
            file.write(nlu_output)
        nlu_js = parsing_json(nlu_output)
        logger.info(f"NLU output: {nlu_js}")
        return nlu_js

class DM():
    def __init__(self):
        pass

    def __call__(self, tracker, intent):
        
        self.info_text = tracker.dictionary(intent)
        dm_text = PROMPTS["DM"] +'\n'+ str(self.info_text)
        dm_output = generate_response_Ollama(dm_text)
        dm_output = dm_output.strip()

        with open("dm_output.txt", "w") as file:
            file.write(dm_output)
        
        logger.debug(f"DM output: {dm_output}")
        action, argument = extract_action_and_argument(dm_output)
        return action, argument
    
class NLG():
    def __init__(self):
        pass

    def __call__(self, action, argument):
        nlg_text = PROMPTS["NLG"] + '\n' + f"{action}({argument})"
        nlg_output = generate_response_Ollama(nlg_text)
        nlg_output = nlg_output.strip()
        return nlg_output

class Dialogue:
    def __init__(self):
        self.tracker = DMTracker()
        self.history = History()
        self.nlu = NLU(self.history)
        self.dm = DM()
        self.nlg = NLG()

    def start(self):
        starting = PROMPTS["START"]
        self.history.add_msg(starting, 'assistant', 'init')
        user_input = input(starting + '\n')
        self.history.add_msg(user_input, 'user', 'input')

        # exit the loop using CTRL+C
        while True:
            
            # get the NLU output
            infos = self.nlu(user_input)
            print(f"NLU: {infos}")
            intent = self.tracker.update(infos)
            logger.info(self.tracker)
            # get the DM output
            action, arg = self.dm(self.tracker, intent)
            logger.info(f'Action: {action}, Argument: {arg}')

            # get the NLG output
            nlg_output = self.nlg(action, arg)
            self.history.add_msg(nlg_output, 'assistant', action)
            
            user_input = input(nlg_output + '\n')
            self.history.add_msg(user_input, 'user', 'input')

def main():
    # args = get_args()
    logging.basicConfig(filename="app.log", encoding="utf-8", filemode="a")
    logger.info("Starting the dialogue")
    dg = Dialogue()
    dg.start()
    print(dg.history.to_msg_history())

if __name__ == "__main__":
    main()
