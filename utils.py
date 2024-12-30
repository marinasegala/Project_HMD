PROMPTS = {
    "START": """Hi, I am your wine assistant. How can I help you?""",

    "Infos": """Identify the user intent from this list: [wine_ordering, paring_food, asking_info, out_of_domain].
If the intent is asking_info, extract the slots values from the input of the user. The slots are: [title_bottle, typology, country, region, color, grape, abv, closure, flavor, style].
""",

    "Food": """Identify the user intent from this list: [wine_ordering, paring_food, asking_info, out_of_domain].
If the intent is paring_food, extract the slots values from the input of the user. The slots are: [title_bottle, typology, food, year, grape, color, style].
""",

    "Order": """Identify the user intent from this list: [wine_ordering, paring_food, asking_info, out_of_domain].
If the intent is wine_ordering, extract the slots values from the input of the user. The slots are: [title_bottle, typology, quantity, address, phone, gift, pagament].
""",

    "NLU": """Do not invent! If values are not present in the user input, and so they are not specified, you have to put 'null' as value in the slot.
Do not assume any value as default! If they are not specified by the user, put 'null' as value. If the user specifies a value, put it in the slot. If the user specifically says that does not know somwthing, put 'unknown' in the slot.
Return only the json object composed as {"intent": "", "slots": {}}. 
""", 

    "PRE-NLU": """Break the user input into multiple sentences based on the following intents:
- wine_ordering, if the user wants to buy wine.
- paring_food, if the user wants to know what food pairs with the wine.
- asking_info, if the user wants to know more about the wine.
- out_of_domain, if the input does not match any of the above.
Only provide the sequences of intents, as follow: ["sentence1", "sentence2", ...]
Return only the list.
""",

    "DM": """You are the Dialogue Manager.
Given the output of the NLU component, you should only generate the next best action from this list:
- request_clarification(slot), if there is a list of possible values for a slot
- provide_list(intent), if there are sufficient slots filled or the user asks for a list of wines
- request_info(slot), if a slot value is missing (null)
- confirmation(intent), if all slots have been filled
Return only the next best action, nothing more""",

    "NLG": """You are the NLG component of a wine bot assistent: you must be very polite.
Given the next best action classified by the Dialogue Manager (DM), you should only generate a lexicalized response for the user.
Possible next best actions are:
- request_clarification(slot): generate an appropriate message, attached to the list of possible values for the slot for a clarification
- provide_list(intent): generate an appropriate message, attached to the list of wines
- request_info(slot): generate an appropriate question to ask the user for the missing slot value
- confirmation(intent): generate an appropriate confirmation message for the user intent"""
}

MODELS = {
    "llama2": "meta-llama/Llama-2-7b-chat-hf",
    "llama3": "meta-llama/Meta-Llama-3-8B-Instruct",
}

TEMPLATES = {
    "llama2": "<s>[INST] <<SYS>>\n{}\n<</SYS>>\n\n{} [/INST]",
    "llama3": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{}<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
}

import requests
import json
import re
from argparse import Namespace
from typing import Tuple

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BatchEncoding,
    PreTrainedTokenizer,
    PreTrainedModel,
)

def load_model(args: Namespace) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        device_map="auto" if args.parallel else args.device, 
        torch_dtype=torch.float32 if args.dtype == "f32" else torch.bfloat16,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    return model, tokenizer  # type: ignore


def generate(
    model: PreTrainedModel,
    inputs: BatchEncoding,
    tokenizer: PreTrainedTokenizer,
    args: Namespace,
) -> str:
    output = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_new_tokens=args.max_new_tokens,
        pad_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(
        output[0][len(inputs.input_ids[0]) :], skip_special_tokens=True
    )

def generate_response_Ollama(prompt, model="llama3.1:70b"):
    
    url = "http://10.234.0.160:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        text = response.json()
        return text.get("response", "")
        # return response.json().get("generated_text", "")
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return ""

def parsing_json(text):
    json_match = re.search(r"{.*}", text, re.DOTALL)

    if json_match:
        extracted_json = json_match.group()
        # Optionally format it without spaces or newlines
        compact_json = json.dumps(json.loads(extracted_json), separators=(',', ':'))
        # convert the json string to a dictionary
        compact_json = json.loads(compact_json)
        return compact_json
