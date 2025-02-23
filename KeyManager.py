import re
import time
import json
from typing import List

splitter = "::"

def getIndexPrefix(index_name: str) -> str:
    return f"~i~{index_name}"

def getPrefixFilter(index_name:str, prefix:str) -> str:
    return f"{getIndexPrefix(index_name)}{splitter}{prefix}"

def createIndexedKey(index_name: str, key: str) -> str:
    return f"{getIndexPrefix(index_name)}{splitter}{key}"

def createIndexedKeyMulti(index_name: str, keys: List[str]) -> List[str]:
    return [createIndexedKey(index_name, k) for k in keys]

def decomposeKey(key: str) -> dict:
    parts = key.split(splitter)
    key_parts = []
    index = None
    
    for part in parts:
        if (part.startswith("~i~")):
            index = part.split("~")[-1]
    else:
        key_parts.append(part)
    
    return {
        "index":index,
        "key":splitter.join(key_parts)
    }

def decomposeKeyMulti(keys: List[str]) -> List[dict]:
    return [decomposeKey[k] for k in keys]