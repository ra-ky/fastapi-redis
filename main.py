from fastapi import FastAPI, HTTPException
from redis import asyncio as redis

app = FastAPI()

pool = redis.ConnectionPool.from_url("redis://localhost")


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    value = None
    async with redis.Redis(connection_pool=pool) as r:
        value = await r.get(f"item:{item_id}")

    if value is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "value": value}


@app.post("/items/{item_id}")
async def write_item(item_id: str, value: str):
    async with redis.Redis(connection_pool=pool) as r:
        value = await r.set(f"item:{item_id}", value)

    return {"item_id": item_id, "value": value}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
