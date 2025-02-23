from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from BaseClasses import *
from typing import List
from KeyManager import *

app = FastAPI()

# Allow CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Define a router with a prefix
router = APIRouter(prefix="/kvstore/v1")
routerV2 = APIRouter(prefix="/kvstore/v2")

# Create a single persistent AsyncClient
async_client = httpx.AsyncClient()

@app.get("/")
async def read_root():
    res = await async_client.get("http://localhost:3000")
    return {
        "backend": res.json()["status"],
        "status": "ok"
    }

@router.get("/")
async def read_api_base():
    res = await async_client.get("http://localhost:3000")
    return {
        "backend": res.json()["status"],
        "status": "ok"
    }

@router.get("/healthz")
async def read_api_healthz():
    res = await async_client.get("http://localhost:3000")
    return {
        "backend": res.json()["status"],
        "status": "ok"
    }

@router.post("/set")
async def set_value(object: KeyValue):
    res = await async_client.post("http://localhost:3000/put", json={"key": object.key, "value": object.value})
    return res.json()

@router.get("/get")
async def get_value(key: str):
    res = await async_client.get(f"http://localhost:3000/get/{key}")
    return res.json()

@router.get("/exists")
async def exists(key: str):
    res = await async_client.get(f"http://localhost:3000/exists/{key}")
    if res.status_code == 404:
        raise HTTPException(status_code=404, detail=res.text)
    return res.json()

@router.post("/mset")
async def mset(object: MultiKeyValue):
    assert len(object.keys) == len(object.values)
    f_arr = [{"type": "put", "key": object.keys[i], "value": object.values[i]} for i in range(len(object.keys))]
    res = await async_client.post("http://localhost:3000/batch", json=f_arr)
    return res.json()

@router.post("/mget")
async def mget(keys: List[str]):
    res = await async_client.post("http://localhost:3000/getall", json=keys)
    return res.json()

@router.post("/delete")
async def delete_value(key: str):
    res = await async_client.delete(f"http://localhost:3000/delete/{key}")
    return res.json()

@router.post("/mdelete")
async def mdelete(keys: List[str]):
    batch_delete = [{"type": "del", "key": key} for key in keys]
    res = await async_client.post("http://localhost:3000/batch", json=batch_delete)
    return res.json()

# Include the router in the app
app.include_router(router)

@routerV2.post("/set")
async def v2_set_value(data: V2KeyValue):
    if (data.index == None or len(data.index) == 0):
        raise HTTPException(422, "You must specify an index.")
    
    i_key = createIndexedKey(data.index, data.key)
    kv = KeyValue(key=i_key, value=data.value)
    return await set_value(kv)
    
@routerV2.post("/get")
async def v2_get_value(data: V2Key):
    if (data.index == None or len(data.index) == 0):
        raise HTTPException(422, "You must specify an index")
    i_key = createIndexedKey(data.index, data.key)
    res = await get_value(i_key)
    if ("error" in res):
        raise HTTPException(404, f"Key '{data.key}' Not Found in Index '{data.index}")
    _v = decomposeKey(res["key"])
    _v["internalKey"] = res["key"]
    _v["value"] = res["value"]
    return _v

@routerV2.post("/exists")
async def v2_exists(data: V2Key):
    if (data.index == None or len(data.index) == 0):
        raise HTTPException(422, "You must specify an index")
    i_key = createIndexedKey(data.index, data.key)
    res = await exists(i_key)    
    return res["exists"]

@routerV2.post("/mget")
async def v2_mget(data:V2MultiKey):
    if (data.index == None or len(data.index) == 0):
        raise HTTPException(422, "You must specify an index.")
    keys = createIndexedKeyMulti(data.index, data.keys)
    res = await mget(keys)
    f_ = []
    for i in res:
        _v = decomposeKey(i["key"])
        _v["internalKey"] = i["key"]
        _v["value"] = i["value"]
        f_.append(_v)
    return f_

@routerV2.post("/mset")
async def v2_mset(data: V2MultiKeyValue):
    if (data.index == None or len(data.index) == 0):
        raise HTTPException(422, "You must specify an index.")
    keys = createIndexedKeyMulti(data.index, data.keys)
    return await mset(MultiKeyValue(keys=keys, values=data.values))

@routerV2.post("/delete")
async def v2_delete(data: V2Key):
    if (data.index == None or len(data.index) == 0):
        raise HTTPException(422, "You must specify an index.")
    
    key = createIndexedKey(data.index, data.key)
    return await delete_value(key)

@routerV2.post("/mdelete")
async def v2_mdelete(data: V2MultiKey):
    if (data.index == None or len(data.index) == 0):
        raise HTTPException(422, "You must specify an index.")
    keys = createIndexedKeyMulti(data.index, data.keys)
    return await mdelete(keys)

@routerV2.post("/prefixFilter")
async def v2_prefixFilter(data: V2PrefixFilter):
    if (data.index == None or len(data.index) == 0):
        raise HTTPException(422, "You must specify an index.")
    prefix = getPrefixFilter(data.index, data.prefix)
    path = f"http://localhost:3000/search_prefix?prefix={prefix}"
    res = await async_client.get(path)
    
    f_ = []
    for i in res.json():
        _v = decomposeKey(i["key"])
        _v["internalKey"] = i["key"]
        _v["value"] = i["value"]
        f_.append(_v)
    return f_
    
@routerV2.post("/filter")
async def v2_filter(data: V2Filter):
    if (data.index == None or len(data.index) == 0):
        raise HTTPException(422, "You must specify an index.")
    prefix = getIndexPrefix(data.index)
    path = f"http://localhost:3000/search_prefix?prefix={prefix}&contains={data.contains}"
    res = await async_client.get(path)
    f_ = []
    for i in res.json():
        _v = decomposeKey(i["key"])
        _v["internalKey"] = i["key"]
        _v["value"] = i["value"]
        f_.append(_v)
    return f_

@routerV2.post("/advancedFilter")
async def v2_advancedFilter(data: V2AdvancedFilter):
    if (data.index == None or len(data.index) == 0):
        raise HTTPException(422, "You must specify an index.")
    prefix = getPrefixFilter(data.index, data.prefix)
    suffix = getPrefixFilter(data.index, data.suffix)
    contains = data.contains if data.contains is not None else "::"
    print(prefix, suffix)
    path = f"http://localhost:3000/search_filter?prefix={prefix}&suffix={suffix}&contains={contains}"
    res = await async_client.get(path)
    
    f_ = []
    for i in res.json():        
        _v = decomposeKey(i["key"])
        _v["internalKey"] = i["key"]
        _v["value"] = i["value"]
        f_.append(_v)
    return f_

app.include_router(routerV2)
# Gracefully close the async client when shutting down the app
@app.on_event("shutdown")
async def shutdown():
    await async_client.aclose()