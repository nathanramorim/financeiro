from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router

app = FastAPI(
    title="Financeiro API",
    description="API RESTful desacoplada para o Assistente Financeiro Inteligente",
    version="1.0.0"
)

# Configuração de CORS para permitir acesso local do frontend Next.js
origins = [
    "http://localhost:3020",
    "http://127.0.0.1:3020",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
