from semanticscholar import SemanticScholar
import os

api_key = os.getenv('API_KEY_SEMANTICSCHOLAR')  # API key
sch = SemanticScholar(api_key=api_key)

papers = sch.get_paper_citations("bef35a17e7b08aa9a3d6cc53d67f09a91aa11fbb")

for paper in papers:
    paper = paper["citingPaper"]

papers = sch.get_paper_references("bef35a17e7b08aa9a3d6cc53d67f09a91aa11fbb")

for paper in papers:
    paper = paper["citedPaper"]
    print(paper["title"])
