from utils import PROMPTS, generate

class NLG():
    def __init__(self, history, model, tokenizer, args, logger):
        self.history = history
        self.model = model
        self.tokenizer = tokenizer
        self.args = args
        self.logger = logger
        pass

    def __call__(self, action, argument):
        last_int = self.history.last_iterations()
        
        nlg_text =  f"{action}({argument})\n" + last_int 

        nlg_text = self.args.chat_template.format(PROMPTS["NLG"], nlg_text)
        nlg_input = self.tokenizer(nlg_text, return_tensors="pt").to(self.model.device)
        nlg_output = generate(self.model, nlg_input, self.tokenizer, self.args)
        self.logger.info(f"NLG: {nlg_text}")
        nlg_output = nlg_output.strip()
        return nlg_output
