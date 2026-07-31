import uvicorn


def main() -> None:
    uvicorn.run("src.api.api:app", host="127.0.0.1", port=8000)
