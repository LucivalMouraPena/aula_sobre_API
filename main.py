"""
API de Cotação de Moedas

Projeto desenvolvido para demonstrar o consumo de uma API externa
utilizando FastAPI e Requests.

Recursos:
- Cotação atual de Dólar (USD)
- Cotação atual de Euro (EUR)
- Cotação atual de Bitcoin (BTC)

Autor: Lucival Moura
"""

from fastapi import FastAPI
import requests

app = FastAPI(
    title="API de Cotação de Moedas",
    description="Consulta cotações em tempo real utilizando a AwesomeAPI.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "mensagem": "Bem-vindo à API de Cotação de Moedas",
        "rotas": [
            "/cotacoes"
        ]
    }


@app.get("/cotacoes")
def obter_cotacoes():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL"

    try:
        response = requests.get(url)
        response.raise_for_status()

        return {
            "mensagem": "Cotações atuais",
            "cotacoes": response.json()
        }

    except requests.RequestException:
        return {
            "erro": "Não foi possível consultar a AwesomeAPI."
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)