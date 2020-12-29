import kampuan as kp
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
app = FastAPI(title="Kampuan project",
              description="Welcome, This is a project using python to do คำผวน by Tanawat C.",
              version="0.0.1",)


@app.get("/")
async def root():
    # return {'message': "Hello welcome to Kampuan API (คำผวน)",
    #         'author': "Tanawat C."}
    response = RedirectResponse(url='/docs')
    return response


@app.get("/vowel/{text}")
def extract_vowel(text: str = 'สวัสดีครับ'):
    return {"input": text,
            "result": kp.extract_vowel(text)}


@app.get("/puan_kam/{text}")
def puan_kam_auto(text: str = 'สวัสดี'):
    return kp.puan_kam(text=text)


@app.get("/puan_kam_all/{text}")
def puan_kam_all(text: str = 'สวัสดี'):
    return kp.puan_kam_all(text=text)

@app.get("/puan_wunnayook/{text}")
def puan_kam_all(text: str = 'สวัสดี'):
    return kp.pun_wunayook(text=text)
