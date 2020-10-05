import kampuan
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!!"}


@app.get("/greet/{name}")
def kampuan_test(name: str = "Anonymous"):
    return {"input": name,
            "message": kampuan.test(name=name)}
