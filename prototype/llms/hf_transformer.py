import torch
from transformers import pipeline
from dotenv import load_dotenv, getenv
from huggingface_hub import login

from proompt_eng import chain_of_thought_v1
from constants import E7_V2_XRIF_PROMPT


load_dotenv()

HF_ACCESS_TOKEN = getenv() # "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"

login(token = HF_ACCESS_TOKEN)


# model_id = "meta-llama/Llama-3.2-1B"

# pipe = pipeline(
#     "text-generation", 
#     model=model_id, 
#     torch_dtype=torch.bfloat16, 
#     device_map="auto",
# )

# pipe("The key to life is")

from transformers import AutoModelForCausalLM, AutoTokenizer
checkpoint = "HuggingFaceTB/SmolLM2-1.7B-Instruct"

device = "cpu"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# for multiple GPUs install accelerate and do `model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto")`
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

messages = [{"role": "user", "content": chain_of_thought_v1(E7_V2_XRIF_PROMPT, "Can you get a coffee to zach's office?")}]
input_text=tokenizer.apply_chat_template(messages, tokenize=False)
inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=250, temperature=0.2, top_p=0.9, do_sample=True)
print(tokenizer.decode(outputs[0]))



