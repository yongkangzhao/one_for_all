from fastapi import FastAPI
from generator import Oneforall
app = FastAPI()

oneforall = Oneforall("results/google/flan-t5-base/model/best-f1/", "results/google/flan-t5-base/tokenizer/best-f1/", "cuda")


@app.get("/generate/{question}/{context}")
async def root(question: str, context: str):
    return oneforall.predict(question, context, 1)
