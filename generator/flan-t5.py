# pip install accelerate
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from pprint import pprint

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large", device_map="auto", torch_dtype=torch.float)

input_text = "Tell me a story about software engineering without using words regarding software engineering."
input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")

outputs = model.generate(input_ids, max_new_tokens=80,
                                                  num_beams=30,
                                                  repetition_penalty=10.0,
                                                  length_penalty=1.0,
                                                  num_return_sequences=5,
                                                  min_length=1,
                                                  num_beam_groups=15,
                                                  diversity_penalty=15.0,
                                                  early_stopping=True)
pprint(tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=True))
