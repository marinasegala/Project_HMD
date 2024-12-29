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
from extractor_csv import *
from component.NLU import NLU
from component.DM import DM
from component.NLG import NLG

logger = logging.getLogger('Dialogue')
logger.setLevel(logging.DEBUG)

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


        logger.info(f"Tracker: {input}")
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
            possible_wine_list = searching_wine(self.tracker, intent)

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
    logging.basicConfig(filename="app.log", encoding="utf-8", filemode="a", level=logging.DEBUG)
    logger.info("Starting the dialogue")
    dg = Dialogue()
    dg.start()
    print(dg.history.to_msg_history())

if __name__ == "__main__":
    main()
