from utils import PROMPTS, generate

class NLG():
    def __init__(self, history, model, tokenizer, args):
        self.history = history
        self.model = model
        self.tokenizer = tokenizer
        self.args = args
        pass

    def __call__(self, action, argument):
        last_int = self.history.to_msg_history()
        last_int = last_int[-5:] if (len(last_int) > 5) else last_int
        last_int = "\n".join([f"{k['role']}: {k['content']}"  for k in last_int])
        
        nlg_text =  f"{action}({argument})\n" + last_int 

        nlg_text = self.args.chat_template.format(PROMPTS["PRE-NLG"], nlg_text)
        nlg_input = self.tokenizer(nlg_text, return_tensors="pt").to(self.model.device)
        nlg_output = generate(self.model, nlg_input, self.tokenizer, self.args)
        # print(f"NLG: {nlg_text}")
        # nlg_output = generate_response_Ollama(nlg_text)
        nlg_output = nlg_output.strip()
        return nlg_output
