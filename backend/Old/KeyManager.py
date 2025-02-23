import re
import time
splitter = "::"

def createNode(name):
    _n = re.sub(r'\W+', '', name)
    return f"NODE{splitter}{_n}"

def createEdge(source, target):
    _s = re.sub(r'\W+', '', source)
    _t = re.sub(r'\W+', '', target)
    return f"EDGE{splitter}{_s}{splitter}{_t}"

def createLink(source, target, link):
    _s = re.sub(r'\W+', '', source)
    _t = re.sub(r'\W+', '', target)
    _l = re.sub(r'\W+', '', link)
    return f"LINK{splitter}{_s}{splitter}{_t}{splitter}{_l}"

def createSymbol(symbol_id):
    return f"SYMBOL{splitter}{symbol_id}"

def createArticle(unique_id):
    return f"ARTICLE{splitter}{unique_id}"

def createArticleLink(article_unique_id, symbol_id, override_ts = None):
    if not override_ts:
        override_ts = time.time()
    return f"ARTICLELINK{splitter}{article_unique_id}{splitter}{symbol_id}{splitter}{override_ts}"

def createSymbolLinkWithArticle(source_symbol_id, dest_symbol_id, article_unique_id, override_ts = None):
    if not override_ts:
        override_ts = time.time()

    
