from semanticscholar import SemanticScholar
import os

api_key = os.getenv('API_KEY_SEMANTICSCHOLAR')  # API key
sch = SemanticScholar(api_key=api_key)

author = sch.get_author(2262347)
print(author)
