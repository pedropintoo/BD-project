from flask import Flask, make_response, render_template, render_template_string, request

from persistency import author, institution, article

app = Flask(__name__)


@app.route("/")
def base():
    return render_template("index.html")


## Authors

@app.route("/authors")
def authors():
    list_authors = author.list_all()
    return render_template("authors/authors.html", authors=list_authors)

@app.route("/authors-list", methods=["GET"])
def authors_list():
    authors = author.list_all()
    return render_template("authors/authors_list.html", authors=authors)

@app.route("/authors/<author_id>", methods=["GET"])
def authors_details(author_id: str):
    author = author.read(author_id)
    return render_template("authors/author_details_view.html", author=author)

@app.route('/search-authors', methods=['GET'])
def search_authors():
    query = request.args.get('query', '').strip()  # Get the search term from the query parameter
    
    if query != "":
        authors = author.filterByName(query)
    else:
        authors = author.list_all()    

    return render_template('authors/authors_list.html', authors=authors)

########

## Institutions

@app.route("/institutions")
def institutions():
    list_institutions = institution.list_all()
    return render_template("institutions/institutions.html", institutions=list_institutions)

@app.route("/institutions-list", methods=["GET"])
def institutions_list():
    institutions = institution.list_all()
    return render_template("institutions/institutions_list.html", institutions=institutions)

@app.route("/institutions/<institution_id>", methods=["GET"])
def institutions_details(institution_id: str):
    institution = institution.read(institution_id)
    return render_template("institutions/institution_details_view.html", institution=institution)

@app.route('/search-institutions', methods=['GET'])
def search_institutions():
    query = request.args.get('query', '').strip()  # Get the search term from the query parameter
    
    if query != "":
        institutions = institution.filterByName(query)
    else:
        institutions = institution.list_all()    

    return render_template('institutions/institutions_list.html', institutions=institutions)

########

## Articles

@app.route("/articles")
def articles():
    list_articles = article.list_all()
    return render_template("articles/articles.html", articles=list_articles)

@app.route("/articles-list", methods=["GET"])
def articles_list():
    articles = article.list_all()
    return render_template("articles/articles_list.html", articles=articles)

@app.route("/articles/<article_id>", methods=["GET"])
def articles_details(article_id: str):
    article = article.read(article_id)
    return render_template("articles/article_details_view.html", article=article)

@app.route('/search-articles', methods=['GET'])
def search_articles():
    query = request.args.get('query', '').strip()  # Get the search term from the query parameter
    
    if query != "":
        articles = article.filterByName(query)
    else:
        articles = article.list_all()    

    return render_template('articles/articles_list.html', articles=articles)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
