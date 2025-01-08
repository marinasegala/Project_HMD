from slots_classes import Ordering, ParingFood, AskInfo
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
    
class Tracker:
    def __init__(self, logger):
        self.possible_intent = ['wine_ordering', 'paring_food', 'asking_info', 'out_of_domain']
        self.intentions = []
        self.ordering = None
        self.paring_food = None
        self.asking_info = None
        self.logger = logger
    
    def update(self, input: dict):
        intent = input["intent"]
        refactoring = []
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
                    refactor = assign_field(self.ordering, field, input[field])
                    refactoring.append(refactor)
                elif 'paring_food' in intent:
                    refactor = assign_field(self.paring_food, field, input[field])
                    refactoring.append(refactor)
                elif 'asking_info' in intent:
                    refactor = assign_field(self.asking_info, field, input[field])
                    refactoring.append(refactor)

        self.logger.info(f"Tracker: {input}")
        return intent, refactoring
    
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