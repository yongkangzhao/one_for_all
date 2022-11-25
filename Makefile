build:
	cd generator ; docker build . -t oneforall:latest

deploy:
	docker run  --name triple_generator --gpus all -d --restart always oneforall python generator.py --prompt_path prompts/prompt.json --host 54.183.139.246 
	docker run  --name sentence_generator --gpus all -d --restart always oneforall python generator_sentence.py --prompt_path prompts/sentence_prompt.json --host 54.183.139.246 

destroy:
	docker stop triple_generator
	docker rm triple_generator
	docker stop sentence_generator
	docker rm sentence_generator