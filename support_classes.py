from intents_classes import *
from support_fn import assign_field

class History():
    def __init__(self):
        self.messages = []
        self.intent = []
        self.roles = []
        self.last_intent = ''
        self.number_last = 5

    def update_number_last(self, num: int):
        self.number_last = num

    def update_last_int(self, intent):
        self.last_intent = intent

    def get_last_int(self):
        return self.last_intent

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
    
    def last_iterations(self):
        last_int = self.to_msg_history()
        last_int = "\n".join([f"{k['role']}: {k['content']}"  for k in last_int])
        return last_int
    
class Tracker():
    def __init__(self, logger):
        self.possible_intent = ['wine_details', 'wine_origin', 'wine_production', 'wine_conservation', 'wine_paring', 'food_paring', 'wine_ordering', 'delivery']
        self.intentions = []
        self.wine_details = None
        self.wine_origin = None
        self.wine_production = None
        self.wine_conservation = None
        self.wine_paring = None
        self.food_paring = None
        self.wine_ordering = None
        self.delivery = None
        self.logger = logger
        self.required_list_user = False
        self.type_for_list = ['wine_details', 'wine_origin', 'wine_production', 'wine_conservation', 'wine_paring', 'food_paring']
    
    def creation (self, input: dict, history: History, update: bool):
        intent = input["intent"]

        if intent == 'out_of_domain' or intent == 'general_info':
            history.update_last_int('')
            return intent, False
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
                self.wine_ordering = Wine_ordering()
            elif 'delivery' in intent:
                self.delivery = Delivery()
        name, counting_slot = self.name_slot_current_intent(intent)
        history.update_last_int(name)

        if update:
            return self.update(input, counting_slot)
        else:
            return intent, False

    def update(self, input: dict, total_slots: int):
        intent = input["intent"]
        input = input["slots"] 
        count = 0
        for field in input:
            if field == 'giving_list_wine' and (input[field] == 'true' or input[field] == 'True' or  input[field] == True or input[field] == 'yes' or input[field] == 'Yes'):
                self.required_list_user = True
            elif input[field] != 'null' and input[field] != None and input[field] != 'None':
                if 'details' in intent:
                    assign_field(self.wine_details, field, input[field], self)
                elif 'origin' in intent:
                    assign_field(self.wine_origin, field, input[field], self)
                elif 'production' in intent:
                    assign_field(self.wine_production, field, input[field], self)
                elif 'conservation' in intent:
                    assign_field(self.wine_conservation, field, input[field], self)
                elif 'wine_paring' in intent:
                    assign_field(self.wine_paring, field, input[field], self)
                elif 'food_paring' in intent:
                    assign_field(self.food_paring, field, input[field], self)
                elif 'ordering' in intent:
                    assign_field(self.wine_ordering, field, input[field], self)
                elif 'delivery' in intent:
                    assign_field(self.delivery, field, input[field], self)
                count += 1
        self.logger.info(f"Tracker: {input}")

        return intent, total_slots == count 
    
    def dictionary(self, intent_ret):
        dict_ret = {}
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
                elif 'delivery' in x:
                    dict_ret = { "intent": x, "slots": self.delivery.__dict__}

                print(f"Dict: {dict_ret}")
                return dict_ret
            
        if intent_ret == 'out_of_domain':
            return {"intent": "out_of_domain"}
        if intent_ret == 'general_info':
            return {"intent": "general_info"}
        
    def name_slot_current_intent(self, intent):
        if 'details' in intent:
            return self.wine_details.name(), len(self.wine_details.__dict__)
        elif 'origin' in intent:
            return self.wine_origin.name(), len(self.wine_origin.__dict__)
        elif 'production' in intent:
            return self.wine_production.name(), len(self.wine_production.__dict__)
        elif 'conservation' in intent:
            return self.wine_conservation.name(), len(self.wine_conservation.__dict__)
        elif 'wine_paring' in intent:
            return self.wine_paring.name(), len(self.wine_paring.__dict__)
        elif 'food_paring' in intent:
            return self.food_paring.name(), len(self.food_paring.__dict__)
        elif 'ordering' in intent:
            return self.wine_ordering.name(), len(self.wine_ordering.__dict__)
        elif 'delivery' in intent:
            return self.delivery.name(), len(self.delivery.__dict__)