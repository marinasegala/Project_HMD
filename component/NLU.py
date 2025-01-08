import logging
from utils import PROMPTS, generate, parsing_json

class Analizer():
    # used for pre-processing the input text - find all the intent possible in the text
    def __init__(self, history, model, tokenizer, args):
        self.history = history
        self.model = model
        self.tokenizer = tokenizer
        self.args = args
        pass
    
    def __call__(self, text):
        # extract all the intent in the text
        last_int = self.history.to_msg_history()
        last_int = last_int[-5:] if (len(last_int) > 5) else last_int
        last_int = "\n".join([f"{k['role']}: {k['content']}"  for k in last_int])
        # logger.info(f"History: {last_int}")
        
        text = last_int + '\n' + text
        text = self.args.chat_template.format(PROMPTS["PRE-NLU"], text)
        pre_nlu_input = self.tokenizer(text, return_tensors="pt").to(self.model.device)
        intents = generate(self.model, pre_nlu_input, self.tokenizer, self.args)


        # intents = generate_response_Ollama(nlu_text)
        print(f"Intents: {intents}")
        # convert the string to a list
        intents = intents.replace("[", "").replace("]", "").replace('"', "").split(",")
        return intents
        

class NLU():
    def __init__(self, history, model, tokenizer, args):
        self.history = history
        self.analizer = Analizer(history, model, tokenizer, args)
        self.model = model
        self.tokenizer = tokenizer
        self.args = args
        pass
    
    def __call__(self, user_input):
        list_intents = self.analizer(user_input) #TODO 
        print(f"List intents: {list_intents}")
        list_int = list_intents[0]
        # match list_int:
        #    case "wine_ordering":
        #        prompt = PROMPTS["Order"]
        #    case "paring_food":
        #        prompt = PROMPTS["Food"]
        #    case "asking_info":
        #        prompt = PROMPTS["Infos"]
        
        # prompt = prompt + '\n' + PROMPTS["NLU"]
        prompt = PROMPTS["NLU2"]
        last_int = self.history.to_msg_history()
        last_int = last_int[-5:] if (len(last_int) > 5) else last_int
        last_int = "\n".join([f"{k['role']}: {k['content']}"  for k in last_int])
        # logger.info(f"History: {last_int}")

        nlu_text = last_int + '\n' + user_input

        nlu_text = self.args.chat_template.format(prompt, nlu_text)
        nlu_input = self.tokenizer(nlu_text, return_tensors="pt").to(self.model.device)
        nlu_output = generate(self.model, nlu_input, self.tokenizer, self.args)

        # nlu_output = generate_response_Ollama(nlu_text)
        nlu_output = nlu_output.strip()

        with open("nlu_output.txt", "w") as file:
            file.write(nlu_output)
        nlu_js = parsing_json(nlu_output)
        # logger.info(f"NLU output: {nlu_js}")
        return nlu_js
