from typing import List, Optional
from pydantic import BaseModel

class KeyValue(BaseModel):
    key: str
    value: str

class MultiKeyValue(BaseModel):
    keys: List[str]
    values: List[str]

class V2Key(BaseModel):
    index:str
    key:str

class V2MultiKey(BaseModel):
    index:str
    keys: List[str]

class V2KeyValue(BaseModel):
    index: str
    key: str
    value: str

class V2MultiKeyValue(BaseModel):
    index: str
    keys: List[str]
    values: List[str]

class V2PrefixFilter(BaseModel):
    index: str
    prefix: str

class V2AdvancedFilter(BaseModel):
    index: str
    prefix: str
    suffix: str
    contains: Optional[str] = None

class V2Filter(BaseModel):
    index: str
    contains: str