build-generator:
	cd generator ; docker build . -t oneforall-generator:latest

build-oneforall:
	cd oneforall ; docker build . -t oneforall-inference:latest

deploy-generator:
	docker run  --name triple_generator --gpus all -d --restart always oneforall-generator python generator.py --prompt_path prompts/prompt.json --host 54.183.139.246 
	docker run  --name sentence_generator --gpus all -d --restart always oneforall-generator python generator_sentence.py --prompt_path prompts/sentence_prompt.json --host 54.183.139.246 

deploy-oneforall:
	docker run  --name oneforall-inference -p 8000:8000 --gpus all -d --restart always oneforall-inference uvicorn main:app --host 0.0.0.0 --port 8000 --reload 

destroy-generator:
	docker stop triple_generator
	docker rm triple_generator
	docker stop sentence_generator
	docker rm sentence_generator

destroy-oneforall:
	docker stop oneforall-inference
	docker rm oneforall-inference

build-all: build-generator build-oneforall

deploy-all: deploy-generator deploy-oneforall

destroy-all: destroy-generator destroy-oneforall

