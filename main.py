from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service import *
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["*"],
)


@app.get("/horoscope/{sign}/full/")
async def horoscope_full(sign: str):
    response = get_full_horoscope(sign=sign)
    return response

@app.get("/horoscope/{sign}/")
async def horoscope(sign: str):
    response = get_horoscope(sign=sign)
    return response



