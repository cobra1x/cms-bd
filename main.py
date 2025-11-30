from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app= FastAPI()
source=[
    "https://ai-legalmate.vercel.app/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=source,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)


app.include_router(router)
