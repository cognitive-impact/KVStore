
@app.post("/graph/v1/add_node")
def add_node(node: Node):
    pass

@app.post("/graph/v1/add_edge")
def add_edge(edge: Edge):
    pass

@app.post("/graph/v1/delete_node")
def delete_node(node: Node):
    pass

@app.post("/graph/v1/delete_edge")
def delete_edge(edge: Edge):
    pass

@app.post("/graph/v1/getEdges")
def get_edges(node: Node):
    pass

@app.post("/news/v1/addSymbol")
def add_symbol(symbol: Symbol, override_if_exists : bool = False):
    pass

@app.post("/news/v1/addArticle")
def add_article(article: Article, override_if_exists: bool = False):
    pass

@app.post("/news/v1/linkArticleToSymbols")
def link_article_to_symbols(link: ArticleLinkRequest):
    pass

@app.post("/news/v1/getArticlesLinkingSymbols")
def get_articles_linking_symbols(symbols: List[Symbol]):
    pass

@app.post("/news/v1/getSymbolsForArticle")
def get_symbols_for_article(article: Article):
    pass

@app.post("/news/v1/getArticlesForSymbol")
def get_articles_for_symbol(symbol: Symbol):
    pass

@app.post("/news/v1/getLatestArticleListForSource/")
def get_latest_articles_for_source(source: Source):
    pass

@app.post("/news/v1/setLatestArticleListForSource")
def set_latest_articles_for_source(source_requested: ArticleListRequest):
    pass