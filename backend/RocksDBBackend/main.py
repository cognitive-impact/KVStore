from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import rocksdb
import json

app = FastAPI()

# Initialize RocksDB
db_opts = rocksdb.Options(create_if_missing=True)
db = rocksdb.DB("rocksdb_store", db_opts)

# ---------------------------- MODELS ----------------------------
class KeyValue(BaseModel):
    key: str
    value: str

class BatchOperation(BaseModel):
    type: str  # "put" or "del"
    key: str
    value: str = None

# ---------------------------- API ENDPOINTS (EXACTLY SAME AS NODE.JS) ----------------------------

@app.get("/")
async def root():
    return {"status": "ok"}

# Get a value by key
@app.get("/get/{key}")
async def get_key(key: str):
    try:
        value = db.get(key.encode())
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found")
        return {"key": key, "value": value.decode()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Put a key-value pair
@app.post("/put")
async def put_key(item: KeyValue):
    try:
        db.put(item.key.encode(), item.value.encode())
        return {"success": True, "key": item.key, "value": item.value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete a key
@app.delete("/delete/{key}")
async def delete_key(key: str):
    try:
        db.delete(key.encode())
        return {"success": True, "key": key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Batch operations
@app.post("/batch")
async def batch_operations(operations: list[BatchOperation]):
    batch = rocksdb.WriteBatch()
    try:
        for op in operations:
            if op.type == "put":
                batch.put(op.key.encode(), op.value.encode())
            elif op.type == "del":
                batch.delete(op.key.encode())

        db.write(batch)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get multiple values by keys (mget)
@app.post("/getall")
async def get_multiple_keys(keys: list[str]):
    try:
        values = db.multi_get([key.encode() for key in keys])
        result = {key: (values[key.encode()].decode() if values[key.encode()] is not None else "Key not found") for key in keys}
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Stream all key-value pairs
@app.get("/stream")
async def stream_keys():
    try:
        it = db.iterkeys()
        it.seek_to_first()
        result = []
        for key in it:
            value = db.get(key)
            result.append({"key": key.decode(), "value": value.decode() if value else "NULL"})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Search by prefix
@app.get("/search_prefix")
async def search_prefix(prefix: str):
    results = []
    try:
        it = db.iterkeys()
        it.seek(prefix.encode())
        for key in it:
            if not key.startswith(prefix.encode()):
                break
            value = db.get(key)
            results.append({"key": key.decode(), "value": value.decode() if value else "NULL"})
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Search with additional filtering
@app.get("/search_filter")
async def search_filter(prefix: str, suffix: str = None, contains: str = None):
    suffix = suffix or prefix + "\xFF"
    results = []
    try:
        it = db.iterkeys()
        it.seek(prefix.encode())
        for key in it:
            if key.decode() > suffix:
                break
            if contains and contains not in key.decode():
                continue
            value = db.get(key)
            results.append({"key": key.decode(), "value": value.decode() if value else "NULL"})
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Check if a key exists
@app.get("/exists/{key}")
async def key_exists(key: str):
    try:
        value = db.get(key.encode())
        return {"key": key, "exists": value is not None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------- RUN THE API ----------------------------
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
