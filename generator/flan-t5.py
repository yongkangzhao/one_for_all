# pip install accelerate
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from pprint import pprint

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large", torch_dtype=torch.float)

# Prompts about occupation
input_text = "My friend is a doctor. He "
input_text = "Ben is a social worker. Everyday, he "
input_text = "People think that a CEO "

# Prompts about traits
input_text = "My mom is a person with charm. What does she do?"
input_text = "My dad is fickleness. What does he like?"
input_text = "She has energeticness. How do people describe her?"
input_text = "Reasons you hate people with manipulativeness. They"

# Prompts about persona
input_text = "He is a luminary."
input_text = "He likes to act as a guardian. He "
input_text = "Why does a researcher do? "

# Prompts about values
input_text = "Achievement is all I want. I wish that "
input_text = "Why do people care about Recognition?"
input_text = "I desire Investigative in life. My dream is "

# Prompts about ncskill
input_text = "He is very good at Divergent thinking. What does he do?"
input_text = "What does Versatility involve?"
input_text = "What does it take to be Diplomacy"

# Prompts about fields of study
input_text = "I study Molecular Biology. I used to "
input_text = "As a Natural Resource Management major, everyday he "
input_text = "What do people say about Mechanical Engineering?"

# Prompts about tasks
input_text = "He Operating Vehicles daily. What does he do?"
input_text = "He likes Operating Vehicles. "
input_text = "What does Working with the Public involve?"
input_text = "What does it take to Working with the Public?"


input_text = "Tell me a story about software engineering without using the word itself.."

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model.to(device)

input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)



outputs = model.generate(input_ids.to(device), max_new_tokens=80,
                                                  num_beams=30,
                                                  repetition_penalty=10.0,
                                                  length_penalty=1.0,
                                                  num_return_sequences=5,
                                                  min_length=10,
                                                  num_beam_groups=15,
                                                  diversity_penalty=15.0,
                                                  early_stopping=True)
pprint(tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=True))
