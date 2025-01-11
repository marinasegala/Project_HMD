from intents_classes import *
from support_fn import assign_field

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
    
class Tracker():
    def __init__(self, logger):
        self.possible_intent = ['wine_details', 'wine_origin', 'wine_production', 'wine_conservation', 'wine_paring', 'food_paring', 'wine_ordering']
        self.intentions = []
        self.wine_details = None
        self.wine_origin = None
        self.wine_production = None
        self.wine_conservation = None
        self.wine_paring = None
        self.food_paring = None
        self.wine_ordering = None
        self.shipping = None
        self.logger = logger
    
    def update(self, input: dict):
        intent = input["intent"]
        assign = None
        if intent in self.possible_intent:
            if intent not in [x for x in self.intentions]:
                self.intentions.append(intent)

                if 'details' in intent:
                    self.wine_details = Wine_details()
                elif 'origin' in intent:
                    self.wine_origin = Wine_origin()
                elif 'production' in intent:
                    self.wine_production = Wine_production()
                elif 'conservation' in intent:
                    self.wine_conservation = Wine_conservation()
                elif 'wine_paring' in intent:
                    self.wine_paring = Wine_paring()
                elif 'food_paring' in intent:
                    self.food_paring = Food_paring()
                elif 'ordering' in intent:
                    self.wine_ordering = Wine_order()

        input = input["slots"] 
        for field in input:
            if input[field] != 'null' and input[field] != None and input[field] != 'None':
                # print(f"Field: {field}")
                
                if 'details' in intent:
                    assign_field(self.wine_details, field, input[field])
                elif 'origin' in intent:
                    assign_field(self.wine_origin, field, input[field])
                elif 'production' in intent:
                    assign_field(self.wine_production, field, input[field])
                elif 'conservation' in intent:
                    assign_field(self.wine_conservation, field, input[field])
                elif 'wine_paring' in intent:
                    assign_field(self.wine_paring, field, input[field])
                elif 'food_paring' in intent:
                    assign_field(self.food_paring, field, input[field])
                elif 'ordering' in intent:
                    assign_field(self.wine_ordering, field, input[field])

        self.logger.info(f"Tracker: {input}")
        return intent
    
    def dictionary(self, intent_ret):
        for x in self.intentions:
            if x == intent_ret:
                if 'details' in x:
                    dict_ret = { "intent": x, "slots": self.wine_details.__dict__}
                elif 'origin' in x:
                    dict_ret = { "intent": x, "slots": self.wine_origin.__dict__}
                elif 'production' in x:
                    dict_ret = { "intent": x, "slots": self.wine_production.__dict__}
                elif 'conservation' in x:
                    dict_ret = { "intent": x, "slots": self.wine_conservation.__dict__}
                elif 'wine_paring' in x:
                    dict_ret = { "intent": x, "slots": self.wine_paring.__dict__}
                elif 'food_paring' in x:
                    dict_ret = { "intent": x, "slots": self.food_paring.__dict__}
                elif 'ordering' in x:
                    dict_ret = { "intent": x, "slots": self.wine_ordering.__dict__}

                print(f"Dict: {dict_ret}")
                return dict_ret