import re
from utils import PROMPTS, generate
from support_fn import parsing_json

class NLU():
    def __init__(self, history, model, tokenizer, args, logger):
        self.history = history
        self.model = model
        self.tokenizer = tokenizer
        self.args = args
        self.logger = logger
        pass
    
    def __call__(self, user_input, slots_empty):
        list_intents = self.extract_intents_list(user_input, slots_empty) 
        self.logger.info(f"List intents: {list_intents}")
        intent = list_intents[0]
        #TODO GESTIRE PIU INTENT
#        print(intent)
        if intent == 'general_info':
            json_output = parsing_json('{"intent": "general_info"}')
        elif intent == 'out_of_domain':
            json_output = parsing_json('{"intent": "out_of_domain"}')
        else:
            json_output = self.extract_slots(user_input, intent)
        
        self.logger.info(f"NLU output: {json_output}")
        
        return json_output

    def extract_intents_list(self, user_input, slots_empty):
        last_interaction = self.history.last_iterations()
        last_intent = self.history.get_last_int()

        self.logger.info(f"History: {last_interaction}")

        if last_intent == 'delivery' or (last_intent == 'wine_ordering' and slots_empty == 0):
            list_intents = PROMPTS["delivery_nlu"] + PROMPTS["list_intents"] + PROMPTS["out_domain"]
        else:
            list_intents = PROMPTS["list_intents"] + PROMPTS["order_nlu"] + PROMPTS["out_domain"]
        #print('\n', list_intents)
        list_intents = PROMPTS["NLU_intents_start"] + list_intents + PROMPTS["NLU_intents_end"]
        #print('RRR ', last_intent, slots_empty)

        text = last_interaction + '\n' + user_input
        text = self.args.chat_template.format(list_intents, text)
        pre_nlu_input = self.tokenizer(text, return_tensors="pt").to(self.model.device)
        intents = generate(self.model, pre_nlu_input, self.tokenizer, self.args)

        # convert the string to a list
        # intents = intents.replace("[", "").replace("]", "").replace('"', "").split(",")
        matches = re.findall(r'\[.*\]', intents)
        if matches:
            intents = eval(matches[0])
            self.logger.info(f"Intents: {intents}")
        else:
            intents = []
            print("No list found in the text.")

        return intents
    
    def extract_slots(self, user_input, intent):
        if intent == "wine_details": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-details"]
        elif intent == "wine_origin": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-origin"]
        elif intent == "wine_production": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-production"]
        elif intent == "wine_conservation": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-conservation"]
        elif intent == "choosing_food": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-paring"]
        elif intent == "having_food": prompt = PROMPTS["NLU_slots"] + PROMPTS["food-paring"]
        elif intent == "wine_ordering": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-ordering"]
        elif intent == "delivery": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-delivery"]
        
        nlu_text = self.history.last_iterations() + '\n' + user_input

        nlu_text = self.args.chat_template.format(prompt, nlu_text)
        nlu_input = self.tokenizer(nlu_text, return_tensors="pt").to(self.model.device)
        nlu_output = generate(self.model, nlu_input, self.tokenizer, self.args)

        nlu_output = nlu_output.strip()

        self.logger.info(f"NLU output: {nlu_output}")
        nlu_js = parsing_json(nlu_output)
        
        return nlu_js
