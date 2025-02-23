from typing import List, Optional
from pydantic import BaseModel

class KeyValue(BaseModel):
    key: str
    value: str

class MultiKeyValue(BaseModel):
    keys: List[str]
    values: List[str]

class Node(BaseModel):
    name: str
    properties: Optional[dict] = None

class Edge(BaseModel):
    source: str
    target: str
    properties: Optional[dict] = None
    bidirectional: Optional[bool] = True

class Source(BaseModel):
    source_name: str
    source_base_url: str
    source_info: Optional[dict] = None

class Symbol(BaseModel):
    symbol_id: str
    info: Optional[dict] = None

class Article(BaseModel):
    unique_id: str
    uri: str
    publish_ts: float
    info: Optional[dict] = None
    override_ts_with_publish_ts: Optional[bool] = True

class ArticleLinkRequest(BaseModel):
    article_unique_id: str
    symbols: List[Symbol]
    link_info: Optional[dict] = None
    override_ts: Optional[float] = None

class ArticleListRequest(BaseModel):
    source_name: str
    latest_list: Optional[List[str]]
    