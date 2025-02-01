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
The slots are: [flavor, grape, color, sparkling, abv, year, typology, giving_list_wine].
""",

    "wine-origin": """The intent extracted is 'wine_origin'. Extract the slots values from the input of the user.
The slots are: [country, region, color, typology, title_bottle, giving_list_wine].
""",

    "wine-production": """The intent extracted is 'wine_production'. Extract the slots values from the input of the user.
The slots are: [grape, abv, closure, typology, giving_list_wine].
""",

    "wine-conservation": """The intent extracted is 'wine_conservation'. Extract the slots values from the input of the user.
The slots are: [fridge, cellar, temperature, typology, giving_list_wine]. Fridge and celler are boolean
""",

    "wine-paring": """The intent extracted is 'choosing_food'. Extract the slots values from the input of the user.
The slots are: [color, style, typology, food, giving_list_wine].
""",

    "food-paring": """The intent extracted is 'having_food'. Extract the slots values from the input of the user.
The slots are: [food, style, abv, giving_list_wine].
""",

    "wine-ordering": """The intent extracted is 'wine_ordering'. Extract the slots values from the input of the user.
The slots are: [typology, quantity, total_budget, title_bottle].
""",

    "wine-delivery": """The intent extracted is 'wine_delivery'. Extract the slots values from the input of the user.
The slots are: [address, phone, gift, kind_pagament].
""",

    "NLU_slots": """You are a component for a wine bot assistant.  Do not invent! If values are not present in the user input, and so they are not specified, you have to put 'null' as value in the slot.
Do not assume any value as default! If they are not specified by the user, put 'null' as value.
If the user specifies a value, put it in the slot. If the user specifically says that does not know somwthing, put 'null' in the slot.
Return only the json object composed as {"intent": "", "slots": {}}.
Return ONLY the json
""",

    "NLU_intents_start": """You are a component for a wine bot assistant.
Break the user input into multiple sentences based on the following intents:""",

    "NLU_intents_end":"""Provide a list of intents as follow: ["intent1", "intent2", ...].
Return ONLY the list of intents, nothing more!
""",

    "prova": """- general_info: if the user wants general informations about a wine.""",

    "list_intents": """
- wine_origin: if the user wants to know more about the origin of a wine or tells the origin of a wine.
- wine_production: if the user wants to know more about the production of a wine.
- wine_conservation: if the user wants to know more about the conservation of a wine: need to be in the fridge, celler or temperature needed.
- choosing_food: if the user has a wine and he wants to pair it with a food.
- wine_details: if the user wants to know general informations or details or characteristics of a wine.
""",
    
    "order_nlu": """- wine_ordering: if the user wants to buy wine.""",

    "delivery_nlu": """- delivery: if the user wants to buy wine.""",

    "out_domain": """
- out_of_domain, if the input does not match any of the above and none of them is predicted.""",

    "DM_start": """You are the Dialogue Manager of a wine bot assistent.
Given the output of the NLU component, you should ONLY generate the next best action from this list: """,

    "DM_end": """\nYou need to write the name of the action with also the correspondings parameters.
Return ONLY the next best action! Nothing more!""",

    "nba": """
- request_info(slot), if a slot value is missing (null)
- goal_assistant(intent), if the intent is equal to out_of_domain
- repeat(slot), if the system needs clarification on a slot value""",

    "give_list": """
- give_list(intent), if the field provide_list in NLU output is True""",

    "confermation": """
- confermation(intent), if all slots have been filled""",

    "listing_wine": """
- provide_list(intent), if the field provide_list in NLU output is True""",

    "delivery": """
- delivery_info(intent), if all slots have been filled""",

    "NLG": """You are the NLG component of a wine bot assistent: you must be very polite.
Given the next best action classified by the Dialogue Manager (DM), you should only generate a lexicalized response for the user.
The response has to match the next best action of the DM.
Possible next best actions are:
""", 

    "request_info_nlg": """
- request_info(slot): generate an appropriate question to ask the user for the missing slot value. DO NOT give suggestions """,

    "nba_nlg": """
- goal_assistant(intent): generate an appropriate message with the domain of the bot
- repeat(slot): generate a message to ask the user to repeat the information""",

    "knowing_title_nlg": """
- request_info(slot): generate an appropriate question to have the title or topology of the wine, or if the user does not know and prefer to say the missing slot value (slot). DO NOT give suggestions.""",
    
    "confermation_nlg": """
- confermation(intent): generate an appropriate confirmation message for the user intent""",

    "listing_wine_nlg": """
- provide_list(intent): generate an appropriate question for propose a list of wine. Only the question: Can i suggest some wine?""",

    "give_list_nlg": """
- give_list(intent): generate an appropriate message for present a list of wine. Only the message: The top three choices I find are:""",


    "delivery_nlg": """
- delivery_info(intent): generate an appropriate message for confirming the delivery information""",

    "NLG_end": """DO NOT give suggestions! Return ONLY the message to the user!""",

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
