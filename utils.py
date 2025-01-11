import argparse
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

PROMPTS = {
    "START": """Hi, I am your wine assistant. How can I help you?""",

    "wine-details": """The intent extracted is 'wine_details'. Extract the slots values from the input of the user.
The slots are: [flavor, grape, color, sparkling, abv, year, typology].
""",

    "wine-origin": """The intent extracted is 'wine_origin'. Extract the slots values from the input of the user.
The slots are: [country, region, typology, title_bottle].
""",

    "wine-production": """The intent extracted is 'wine_production'. Extract the slots values from the input of the user.
The slots are: [grape, abv, closure].
""",

    "wine-conservation": """The intent extracted is 'wine_conservation'. Extract the slots values from the input of the user.
The slots are: [fridge, cellar, temperature].
""",

    "wine-paring": """The intent extracted is 'wine_paring'. Extract the slots values from the input of the user.
The slots are: [style, color, typology].
""",

    "food-paring": """The intent extracted is 'food_paring'. Extract the slots values from the input of the user.
The slots are: [food, style, abv].
""",

    "wine-ordering": """The intent extracted is 'wine_ordering'. Extract the slots values from the input of the user.
The slots are: [typology, color, quantity, budget, title_bottle].
""",

    "NLU": """You are a component for a wine bot assistant.  Do not invent! If values are not present in the user input, and so they are not specified, you have to put 'null' as value in the slot.
Do not assume any value as default! If they are not specified by the user, put 'null' as value.
If the user specifies a value, put it in the slot. If the user specifically says that does not know somwthing, put 'null' in the slot.
Return only the json object composed as {"intent": "", "slots": {}}.
Return ONLY the json
""", 

    "PRE-NLU": """Break the user input into multiple sentences based on the following intents:
- wine_details: if the user wants to know more about the characteristics of a wine.
- wine_origin: if the user wants to know more about the origin of a wine.
- wine_production: if the user wants to know more about the production of a wine.
- wine_conservation: if the user wants to know more about the conservation of a wine.
- wine_paring: if the user has a wine and he wants to pair it with a food.
- food_paring: if the user has a dish and he wants to pair it with a wine.
- wine_ordering: if the user wants to buy wine.
Only provide the sequences of intents, as follow: ["sentence1", "sentence2", ...]
Return only the list.
""",

    "PRE_NLU": """You are a component for a wine bot assistant.
Break the user input into multiple sentences based on the following intents:
- wine_details: if the user wants to know more about the characteristics of a wine or he wants general informations about it.
- wine_origin: if the user wants to know more about the origin of a wine.
- wine_production: if the user wants to know more about the production of a wine.
- wine_conservation: if the user wants to know more about the conservation of a wine.
- wine_paring: if the user has a wine and he wants to pair it with a food.
- food_paring: if the user has a dish and he wants to pair it with a wine.
- wine_ordering: if the user wants to buy wine.
- out_of_domain, if the input does not match any of the above and none of them is predicted.
Provide a list of intents as follow: ["intent1", "intent2", ...].
Return ONLY the list of intents, nothing more!
""",

    "DM": """You are the Dialogue Manager of a wine bot assistent.
Given the output of the NLU component, you should only generate the next best action from this list:
- request_info(slot), if a slot value is missing (null)
- confirmation(intent), if all slots have been filled
- request_clarification(slot), if there is a list of possible values for a slot
- provide_list(intent), if there are sufficient slots filled or the user asks for a list of wines
Return only the next best action, nothing more""",

    "DM2": """You are the Dialogue Manager of a wine bot assistent.
Given the output of the NLU component, you should ONLY generate the next best action from this list:
- provide_list(intent), if there are sufficient slots filled or the user asks for a list of wines
- request_info(slot), if a slot value is missing (null)
- confirmation(intent), if all slots have been filled
You need to write the name of the action with also the correspondings parameters.
Return ONLY the next best action! """,

    "NLG": """You are the NLG component of a wine bot assistent: you must be very polite.
Given the next best action classified by the Dialogue Manager (DM), you should only generate a lexicalized response for the user.
Possible next best actions are:
- provide_list(intent), if there are sufficient slots filled or the user asks for a list of wines
- request_info(slot), if a slot value is missing (null)
- confirmation(intent), if all slots have been filled"""
}

MODELS = {
    "llama2": "meta-llama/Llama-2-7b-chat-hf",
    "llama3": "meta-llama/Meta-Llama-3-8B-Instruct",
}

TEMPLATES = {
    "llama2": "<s>[INST] <<SYS>>\n{}\n<</SYS>>\n\n{} [/INST]",
    "llama3": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{}<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
}

def get_args() -> Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m query_model",
        description="Query a specific model with a given input.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "model_name",
        type=str,
        choices=list(MODELS.keys()),
        help="The model to query.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="The device to use for the model.",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Split the model across multiple devices.",
    )
    parser.add_argument(
        "--dtype",
        type=str,
        choices=["f32", "bf16"],
        default="bf16",
        help="The data type to use for the model.",
    )
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=128,
        help="The maximum sequence length to use for the model.",
    )

    parsed_args = parser.parse_args()
    parsed_args.chat_template = TEMPLATES[parsed_args.model_name]
    parsed_args.model_name = MODELS[parsed_args.model_name]

    return parsed_args

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