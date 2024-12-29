from utils import PROMPTS, generate_response_Ollama


class NLG():
    def __init__(self):
        pass

    def __call__(self, action, argument):
        nlg_text = PROMPTS["NLG"] + '\n' + f"{action}({argument})"
        print(f"NLG: {nlg_text}")
        nlg_output = generate_response_Ollama(nlg_text)
        nlg_output = nlg_output.strip()
        return nlg_output