from intents_classes import *
from support_fn import assign_field

class History():
    def __init__(self):
        self.messages = []
        self.list_wine = []
        self.index_list = []
        self.intent = []
        self.roles = []
        self.last_intent = ''
        self.number_last = 5
        self.other_int = []

    def update_number_last(self, num: int):
        self.number_last = num

    def update_last_int(self, intent):
        self.last_intent = intent

    def get_last_int(self):
        return self.last_intent
    
    def insert_other_int(self, intent):
        last_int = self.get_last_int()
        if intent not in self.other_int and intent != last_int:
            self.other_int.append(intent)

    def get_other_int(self):
        return self.other_int
    
    def remove_other_int(self):
        if len(self.other_int) > 0:
            self.other_int = self.other_int[1:]

    def add_msg(self, msg, role, intent):
        self.roles.append(role)
        self.messages.append(msg)
        self.intent.append(intent)

    def add_msg_complete(self, msg):
        self.index_list.append(len(self.messages))
        self.list_wine.append(msg)

    def clear(self):
        self.messages = []
        self.intent = []
        self.roles = []
        self.last_intent = ''
        self.number_last = 5
        self.other_int = []
    
    def get_history(self):
        # add to msg the list of wines
        for i in range(len(self.index_list)):
            # insert the msg in the index specified by index_list
            self.messages.insert(self.index_list[i], self.list_wine[i])
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
        self.possible_intent = ['wine_details', 'wine_origin', 'wine_production', 'wine_conservation', 'choosing_food', 'wine_ordering', 'delivery']
        self.intentions = []
        self.wine_details = None
        self.wine_origin = None
        self.wine_production = None
        self.wine_conservation = None
        self.choosing_food = None
        self.wine_ordering = None
        self.delivery = None
        self.logger = logger
        self.required_list_user = False
        self.type_for_list = ['wine_details', 'wine_origin', 'wine_production', 'wine_conservation', 'choosing_food']
    
    def creation (self, input: dict, history: History, update: bool):
        intent = input["intent"]

        if intent == 'out_of_domain':
            history.update_last_int('')
            return intent, 1, 0 
        
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
            elif 'choosing_food' in intent:
                self.choosing_food = Wine_paring()
            elif 'ordering' in intent:
                self.wine_ordering = Wine_ordering()
            elif 'delivery' in intent:
                self.delivery = Delivery()
        name, counting_slot = self.name_slot_current_intent(intent)
        history.update_last_int(name)

        if update:
            return self.update(input, counting_slot)
        else:
            return intent, 1, 0

    def update(self, input: dict, total_slots: int):
        intent = input["intent"]
        input = input["slots"]
        count = 0
        for field in input:
            if field == 'giving_list_wine' and (input[field] == 'true' or input[field] == 'True' or  input[field] == True or input[field] == 'yes' or input[field] == 'Yes'):
                self.required_list_user = True
            elif input[field] != 'null' and input[field] != None and input[field] != 'None':
                if 'details' in intent:
                    assigned, up_num = assign_field(self.wine_details, field, input[field], self)
                elif 'origin' in intent:
                    assigned, up_num = assign_field(self.wine_origin, field, input[field], self)
                elif 'production' in intent:
                    assigned, up_num = assign_field(self.wine_production, field, input[field], self)
                elif 'conservation' in intent:
                    assigned, up_num = assign_field(self.wine_conservation, field, input[field], self)
                elif 'choosing_food' in intent:
                    assigned, up_num = assign_field(self.choosing_food, field, input[field], self)
                elif 'ordering' in intent:
                    assigned, up_num = assign_field(self.wine_ordering, field, input[field], self)
                elif 'delivery' in intent:
                    assigned, up_num = assign_field(self.delivery, field, input[field], self)
                if assigned:
                    count += up_num
        self.logger.info(f"Tracker: {input}")

        return intent, total_slots, count 
    
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
                elif 'choosing_food' in x:
                    dict_ret = { "intent": x, "slots": self.choosing_food.__dict__}
                elif 'ordering' in x:
                    dict_ret = { "intent": x, "slots": self.wine_ordering.__dict__}
                elif 'delivery' in x:
                    dict_ret = { "intent": x, "slots": self.delivery.__dict__}

                # print(f"Dict: {dict_ret}")
                return dict_ret
            
        if intent_ret == 'out_of_domain':
            return {"intent": "out_of_domain"}
        
    def name_slot_current_intent(self, intent):
        if 'details' in intent:
            return self.wine_details.name(), len(self.wine_details.__dict__)
        elif 'origin' in intent:
            return self.wine_origin.name(), len(self.wine_origin.__dict__)
        elif 'production' in intent:
            return self.wine_production.name(), len(self.wine_production.__dict__)
        elif 'conservation' in intent:
            return self.wine_conservation.name(), len(self.wine_conservation.__dict__)
        elif 'choosing_food' in intent:
            return self.choosing_food.name(), len(self.choosing_food.__dict__)
        elif 'ordering' in intent:
            return self.wine_ordering.name(), len(self.wine_ordering.__dict__)
        elif 'delivery' in intent:
            return self.delivery.name(), len(self.delivery.__dict__)
