from fastapi import FastAPI, Request
from datetime import datetime
import pandas as pd
import os

app = FastAPI()

ARCHIVO = "data/archivo.csv"

@app.get("/")
def raiz():
    return {"mensaje": "API de ejemplo para Grafana desde GitHub + Render"}

@app.get("/datos")
def leer_datos(request: Request):
    if not os.path.exists(ARCHIVO):
        return {"error": f"Archivo '{ARCHIVO}' no encontrado."}

    df = pd.read_csv(ARCHIVO)
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors='coerce')
    df = df.dropna(subset=["TIMESTAMP"])

    from_ts = request.query_params.get("from")
    to_ts = request.query_params.get("to")
    if from_ts and to_ts:
        from_dt = datetime.fromisoformat(from_ts.replace("Z", ""))
        to_dt = datetime.fromisoformat(to_ts.replace("Z", ""))
        df = df[(df["TIMESTAMP"] >= from_dt) & (df["TIMESTAMP"] <= to_dt)]

    return df.to_dict(orient="records")