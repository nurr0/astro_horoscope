from service import *
from fastapi import FastAPI, HTTPException
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

from settings import *
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    ),
    Middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]
    )
]

app = FastAPI(middleware=middleware)

# Словарь для хранения количества запросов от каждого IP-адреса
ip_requests = {}

# Время, в течение которого можно делать определенное количество запросов
time_interval = timedelta(seconds=TIME_INTERVAL_FOR_MAX_REQUESTS)

# Максимальное количество запросов за время time_interval
max_requests = MAX_REQUESTS

@app.middleware("http")
async def rate_limit(request, call_next):
    # Получаем IP-адрес запроса
    ip_address = request.client.host

    # Если IP-адрес еще не зарегистрирован в словаре, то добавляем его
    if ip_address not in ip_requests:
        ip_requests[ip_address] = []

    # Удаляем запросы из списка, которые старше time_interval
    current_time = datetime.now()
    ip_requests[ip_address] = [r for r in ip_requests[ip_address] if r + time_interval > current_time]

    # Если количество запросов больше, чем максимальное, то выкидываем исключение HTTP 429 Too Many Requests
    if len(ip_requests[ip_address]) >= max_requests:
        return JSONResponse(content={"detail": "Too many requests"}, status_code=429)

    # Добавляем текущий запрос в список запросов от текущего IP-адреса
    ip_requests[ip_address].append(current_time)

    # Вызываем следующий middleware в цепочке
    response = await call_next(request)
    return response

@app.get("/horoscope/{sign}/full/")
async def horoscope_full(sign: str):
    response = get_full_horoscope(sign=sign)
    return response


@app.get("/horoscope/{sign}/")
async def horoscope(sign: str):
    response = get_horoscope(sign=sign)
    return response


@app.get("/name/{name}/")
async def name_meaning(name: str):
    response = get_name_meaning(name)
    return response
