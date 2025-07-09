# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api import endpoints
import os

app = FastAPI(
    title="AI Learning Coach API",
    description="API for the Personalized Adaptive Learning Assistant",
    version="0.1.0"
)

# 配置 CORS 中间件，允许所有来源的请求，方便本地开发
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含 API 路由
app.include_router(endpoints.router, prefix="/api")

# 配置静态文件目录，用于提供生成的 PDF
os.makedirs("data/learning_materials", exist_ok=True)
app.mount("/materials", StaticFiles(directory="data/learning_materials"), name="materials")


@app.get("/", summary="Root Endpoint", description="A simple hello world endpoint to check if the server is running.")
async def read_root():
    return {"message": "Welcome to the AI Learning Coach API!"}