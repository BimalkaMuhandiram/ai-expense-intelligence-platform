from fastapi import FastAPI

app = FastAPI(title="AI Expense Intelligence API")


@app.get("/health")
def health_check():
    return {"status": "ok"}