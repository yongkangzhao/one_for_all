build:
	cd generator ; docker build . -t oneforall

deploy:
	docker run  --name triple_generator --gpus all -d --restart always  oneforall --prompt_path prompts/prompt.json --host 54.183.139.246 

destroy:
	docker stop triple_generator
	docker rm triple_generator