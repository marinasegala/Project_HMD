from utils import PROMPTS, generate

class NLG():
    def __init__(self, history, model, tokenizer, args, logger):
        self.history = history
        self.model = model
        self.tokenizer = tokenizer
        self.args = args
        self.logger = logger
        pass

    def __call__(self, action, argument, intent, list_possible_wine = []):
        last_int = self.history.last_iterations()
        
        nlg_text =  f"{action}({argument})\n" + last_int 

        if intent == "wine_ordering": nba_add = PROMPTS['list_nba_nlg'] + PROMPTS['shopper_nlg']
        elif intent == "general_info": nba_add = PROMPTS['general_info'] + PROMPTS['list_nba_nlg']
        else: nba_add = PROMPTS['list_nba_nlg'] + PROMPTS['confermation']

        if list_possible_wine != []:
            nba_add = PROMPTS['list_wine'] + nba_add
         
        prompt = PROMPTS["NLG"] + nba_add
        
        nlg_text = self.args.chat_template.format(prompt, nlg_text)
        nlg_input = self.tokenizer(nlg_text, return_tensors="pt").to(self.model.device)
        nlg_output = generate(self.model, nlg_input, self.tokenizer, self.args)
        self.logger.info(f"NLG: {nlg_text}")
        nlg_output = nlg_output.strip()
        return nlg_output
