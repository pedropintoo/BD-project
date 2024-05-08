from flask import Flask, make_response, render_template, render_template_string, request

from persistency import author

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
    query = request.args.get('query', '')  # Get the search term from the query parameter
    authors = author.filterByName(query)
    return render_template('authors/authors_list.html', authors=authors)

########

if __name__ == "__main__":
    app.run(debug=True, port=8080)
