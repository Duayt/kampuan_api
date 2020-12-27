import kampuan as kp
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def root():
    return "see /docs"


@app.get("/user/greet/{name}")
def kampuan_test(name: str = "Anonymous"):
    return {"input": name,
            "message": kp.test(name=name)}


@app.get("/vowel/{phrase}")
def extract_vowel(phrase: str = 'สวัสดีครับ'):
    return {"input": phrase,
            "result": kp.extract_vowel(phrase)}
