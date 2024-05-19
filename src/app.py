from flask import Flask, jsonify, make_response, render_template, render_template_string, request

from persistency import author, institution, article, topic, journal

from persistency.author import Author
from persistency.session import create_connection

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
def author_details(author_id: str):
    author_details = author.read(author_id)
    template = "authors/author_details_view.html" if not request.args.get("edit") else "authors/authors_details_form.html"
    return render_template(template, author=author_details)

@app.route('/search-authors', methods=['GET'])
def search_authors():
    query = request.args.get('query', '').strip()
    if query:
        authors = author.filterByName(query)
    else:
        authors = author.list_all()
    return render_template('authors/authors_list.html', authors=authors)

@app.route("/authors/<author_id>", methods=["DELETE"])
def author_delete(author_id: str):
    try:
        print(f"Deleting author {author_id}")
        author.delete(author_id)
        response = make_response()
        response.headers["HX-Trigger"] = "refreshAuthorList"
        return response
    except Exception as ex:
        r = make_response(render_template_string(f"{ex}"))
        return r

@app.route("/authors/new", methods=["GET"])
def new_author_details():
    return render_template("authors/authors_details_form.html")

@app.route("/authors", methods=["POST"])
def save_author_details():
    data = request.form
    AuthorID = author.generate_author_id(data.get('Name'),data.get('InstitutionID')) # USE A HASH FUNCTION TO GENERATE A ID WITH 10 NUMBERS
    print("NEW AAUTHOR ID GENERATED")
    print(AuthorID)
    new_author = author.Author(
        AuthorID=AuthorID,
        Name=data.get('Name'),
        Url=data.get('Url'),
        ORCID=data.get('ORCID'),
        InstitutionID=data.get('InstitutionID')
    )
    print("NEW Author Added")
    try:
        author.create(new_author)
        response = make_response()
    except Exception:
        print(new_author)
        response = make_response(render_template("authors/authors_details_form.html", author=new_author, warning='ERROR'))

    print(new_author)
    response.headers["HX-Trigger"] = "refreshAuthorList"
    return response

@app.route("/authors/<author_id>", methods=["POST"])
def author_update(author_id: str):
    data = request.form
    InstitutionID = author.get_institution_id(data.get('InstitutionName'))
    new_author = author.AuthorDetails(
        AuthorID=author_id,
        Name=data.get('Name'),
        Url=data.get('Url'),
        ORCID=data.get('ORCID'),
        InstitutionID=InstitutionID,
        InstitutionName=data.get('InstitutionName'),
        ArticlesCount=data.get('ArticlesCount')
    )
    try:
        print("UPDATE")
        author.update(author_id, new_author)
        response = make_response(author_details(author_id))
    except Exception:
        print(new_author)
        response = make_response(render_template("authors/authors_details_form.html", author=new_author, warning='ERROR'))
    
    response.headers["HX-Trigger"] = "refreshAuthorList"
    return response

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
def institution_details(institution_id: str):
    institution_details = institution.read(institution_id)
    template = "institutions/institution_details_view.html" if not request.args.get("edit") else "institutions/institutions_details_form.html"
    return render_template(template, institution=institution_details)

@app.route('/search-institutions', methods=['GET'])
def search_institutions():
    query = request.args.get('query', '').strip()  # Get the search term from the query parameter
    
    if query:
        institutions = institution.filterByName(query)
    else:
        institutions = institution.list_all()    
    return render_template('institutions/institutions_list.html', institutions=institutions)

@app.route("/institutions/<institution_id>", methods=["DELETE"])
def institution_delete(institution_id: str):
    try:
        print(f"Deleting institution {institution_id}")
        institution.delete(institution_id)
        response = make_response()
        response.headers["HX-Trigger"] = "refreshInstitutionList"
        return response
    except Exception as ex:
        r = make_response(render_template_string(f"{ex}"))
        print(ex)
        return r

@app.route("/institutions/new", methods=["GET"])
def new_institution_details():
    return render_template("institutions/institutions_details_form.html")

@app.route("/institutions", methods=["POST"])
def save_institution_details():
    data = request.form
    InstitutionID = institution.generate_institution_id(data.get('Name'),data.get('Address')) # USE A HASH FUNCTION TO GENERATE A ID WITH 10 NUMBERS
    print("NEW INSTITUTION ID GENERATED")
    print(InstitutionID)
    new_institution = institution.Institution(
        InstitutionID=InstitutionID,
        Name=data.get('Name'),
        Address=data.get('Address')
    )
    print("NEW Institution Added")
    try:
        institution.create(new_institution)
        response = make_response()
    except Exception:
        print(new_institution)
        response = make_response(render_template("institutions/institutions_details_form.html", institution=new_institution, warning='ERROR'))

    print(new_institution)
    response.headers["HX-Trigger"] = "refreshInstitutionList"
    return response

@app.route("/institutions/<institution_id>", methods=["POST"])
def institution_update(institution_id: str):
    data = request.form

    new_institution = institution.AuthorDetails(
        InstitutionID=institution_id,
        Name=data.get('Name'),
        Address=data.get('Address')
    )
    try:
        print("UPDATE")
        institution.update(institution_id, new_institution)
        response = make_response(institution_details(institution_id))
    except Exception:
        print(new_institution)
        response = make_response(render_template("institutions/institutions_details_form.html", institution=new_institution, warning='ERROR'))
    
    response.headers["HX-Trigger"] = "refreshInstitutionList"
    return response



# Testing purpose
@app.route('/search-prefix', methods=['GET'])
def search_prefix():
    print("Searching prefix")
    query = request.args.get('query', '').strip()  # Get the search term from the query parameter
    
    if query != "":
        institutions_names = institution.search_institution_by_prefix(query)
    else:
        institutions_names = []    
         
    # Renderiza um fragmento HTML com os resultados
    return render_template('institutions/institutions_fragment.html', institutions=institutions_names)


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

########

## Topics

@app.route("/topics")
def topics():
    list_topics = topic.list_all()
    return render_template("topics/topics.html", topics=list_topics)

@app.route("/topics-list", methods=["GET"])
def topics_list():
    topics = topic.list_all()
    return render_template("topics/topics_list.html", topics=topics)

@app.route("/topics/<topic_id>", methods=["GET"])
def topics_details(topic_id: str):
    topic = topic.read(topic_id)
    return render_template("topics/topic_details_view.html", topic=topic)

@app.route('/search-topics', methods=['GET'])
def search_topics():
    query = request.args.get('query', '').strip()  # Get the search term from the query parameter
    
    if query != "":
        topics = topic.filterByName(query)
    else:
        topics = topic.list_all()    

    return render_template('topics/topics_list.html', topics=topics)

########

## Journals

@app.route("/journals")
def journals():
    list_journals = journal.list_all()
    return render_template("journals/journals.html", journals=list_journals)

@app.route("/journals-list", methods=["GET"])
def journals_list():
    journals = journal.list_all()
    return render_template("journals/journals_list.html", journals=journals)

@app.route("/journals/<journal_id>", methods=["GET"])
def journals_details(journal_id: str):
    journal = journal.read(journal_id)
    return render_template("journals/journal_details_view.html", journal=journal)

@app.route('/search-journals', methods=['GET'])
def search_journals():
    query = request.args.get('query', '').strip()  # Get the search term from the query parameter
    
    if query != "":
        journals = journal.filterByName(query)
    else:
        journals = journal.list_all()    

    return render_template('journals/journals_list.html', journals=journals)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
