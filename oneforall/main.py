from generator import Oneforall
oneforall = Oneforall("results/google/flan-t5-base/model/best-f1/", "results/google/flan-t5-base/tokenizer/best-f1/", "cuda")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate/{question}/{context}")
async def root(question: str, context: str):
    return oneforall.predict(question, context, 1)
