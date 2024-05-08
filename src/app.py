from flask import Flask, make_response, render_template, render_template_string, request

from persistence import customers
from persistence.customers import CustomerDetails

app = Flask(__name__)


@app.route("/")
def base():
    authors = authors.list_all()
    return render_template("index.html", authors=authors)

@app.route("/authors-list", methods=["GET"])
def author_list():
    authors = authors.list_all()
    return render_template("authors_list.html", authors=authors)

@app.route("/authors/<author_id>", methods=["GET"])
def author_details(author_id: str):
    author = authors.read(author_id)
    template = "author_details_view.html"
    return render_template(template, author=author)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
