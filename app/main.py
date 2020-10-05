import kampuan as kp

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!!!!!!"}


@app.get("/user/greet/{name}")
def kampuan_test(name: str = "Anonymous"):
    return {"input": name,
            "message": kp.test(name=name)}


@app.get("/vowel/{phrase}")
def extract_vowel(phrase: str = 'สวัสดีครับ'):
    return kp.extract_vowel(phrase)
