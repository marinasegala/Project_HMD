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
    
    def __call__(self, user_input):
        list_intents = self.extract_intents_list(user_input) 
        self.logger.info(f"List intents: {list_intents}")
        list_int = list_intents[0]

        json_output = self.extract_slots(user_input, list_int)
        self.logger.info(f"NLU output: {json_output}")
        return json_output

    def extract_intents_list(self, user_input):
        last_int = self.history.last_iteration()
        self.logger.info(f"History: {last_int}")
        
        text = last_int + '\n' + text
        text = self.args.chat_template.format(PROMPTS["NLU_intents"], text)
        pre_nlu_input = self.tokenizer(text, return_tensors="pt").to(self.model.device)
        intents = generate(self.model, pre_nlu_input, self.tokenizer, self.args)

        # convert the string to a list
        # intents = intents.replace("[", "").replace("]", "").replace('"', "").split(",")
        matches = re.findall(r'\[.*\]', intents)
        if matches:
            intents = eval(matches[0])
            self.logger.info(f"Intents: {intents}")
            print(type(intents))
        else:
            intents = []
            print("No list found in the text.")

        return intents
    
    def extract_slots(self, user_input, list_int):
        if list_int == "wine_details": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-details"]
        elif list_int == "wine_origin": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-origin"]
        elif list_int == "wine_production": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-production"]
        elif list_int == "wine_conservation": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-conservation"]
        elif list_int == "wine_paring": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-paring"]
        elif list_int == "food_paring": prompt = PROMPTS["NLU_slots"] + PROMPTS["food-paring"]
        elif list_int == "wine_ordering": prompt = PROMPTS["NLU_slots"] + PROMPTS["wine-ordering"]
        else: return parsing_json('{"intent": "out_of_domain"}')
        
        nlu_text = self.history.last_iteration() + '\n' + user_input

        nlu_text = self.args.chat_template.format(prompt, nlu_text)
        nlu_input = self.tokenizer(nlu_text, return_tensors="pt").to(self.model.device)
        nlu_output = generate(self.model, nlu_input, self.tokenizer, self.args)

        nlu_output = nlu_output.strip()

        self.logger.info(f"NLU output: {nlu_output}")
        nlu_js = parsing_json(nlu_output)
        
        return nlu_js
