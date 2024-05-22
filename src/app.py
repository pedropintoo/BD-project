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


# list authors
@app.route("/authors-list", methods=["GET"])
def authors_list():
    authors = author.list_all()
    return render_template("authors/authors_list.html", authors=authors)

@app.route("/authors-list-article-count", methods=["GET"])
def authors_list_by_article_count():
    authors = author.list_all_by_article_count()
    return render_template("authors/authors_list.html", authors=authors)

# show or edit specific author
@app.route("/authors/<author_id>", methods=["GET"])
def author_details(author_id: str):
    author_details = author.read(author_id)
    template = "authors/author_details_view.html" if not request.args.get("edit") else "authors/author_details_form.html"
    return render_template(template, author=author_details, author_id=author_id)

# delete author
@app.route("/authors/<author_id>", methods=["DELETE"])
def author_delete(author_id: str):
    try:
        print(f"Deleting author {author_id}")
        author.delete(author_id)
        response = make_response()
        response.headers["HX-Trigger"] = "refreshAuthorList" # refresh the author list
        return response
    except Exception as ex:
        r = make_response(render_template_string(f"{ex}"))
        return r

# search authors
@app.route('/search-authors', methods=['GET'])
def search_authors():
    query = request.args.get('query', '').strip()   # Get the search term from the query parameter
    if query:
        authors = author.filterByName(query)
    else:
        authors = author.list_all()
    return render_template('authors/authors_list.html', authors=authors)

# form to create new author
@app.route("/authors/new", methods=["GET"])
def new_author_details():
    return render_template("authors/author_details_form.html")

@app.route("/authors", methods=["POST"]) # publish new author
def save_author_details():
    data = request.form
    author_id = author.generate_author_id(data.get('Name'), data.get('Url'), data.get('ORCID'), data.get('InstitutionName')) # USE A HASH FUNCTION TO GENERATE A ID WITH 10 NUMBERS

    new_author = author.AuthorForm(
        Name=data.get('Name'),
        Url=data.get('Url'),
        ORCID=data.get('ORCID'),
        InstitutionName=data.get('InstitutionName')
    )

    try:
        author.create(author_id, new_author)
        response = make_response()
        print("NEW AUTHOR ADDED")
        print(new_author)
    except Exception as e:
        warning_message = str(e.args[1]).split("(50000)")[-2].split("]")[-1].strip() if len(e.args) > 1 else 'ERROR'
        response = make_response(render_template("authors/author_details_form.html", author=new_author, warning=warning_message))
        print(e)
        print("ERROR CREATING AUTHOR")
        print(new_author)
        
    response.headers["HX-Trigger"] = "refreshAuthorList"
    return response    

# update author
@app.route("/authors/<author_id>", methods=["POST"])
def author_update(author_id: str):
    data = request.form

    new_author = author.AuthorForm(
        Name=data.get('Name'),
        Url=data.get('Url'),
        ORCID=data.get('ORCID'),
        InstitutionName=data.get('InstitutionName')
    )

    try:
        author.update(author_id, new_author)
        print("UPDATE AUTHOR")
        response = make_response(author_details(author_id))
    except Exception as e:
        print(new_author)
        warning_message = str(e.args[1]).split("(50000)")[-2].split("]")[-1].strip() if len(e.args) > 1 else 'ERROR'
        response = make_response(render_template("authors/author_details_form.html", author=new_author, author_id=author_id, warning=warning_message))
    
    response.headers["HX-Trigger"] = "refreshAuthorList"
    return response

########

## Institutions

@app.route("/institutions")
def institutions():
    list_institutions = institution.list_all()
    return render_template("institutions/institutions.html", institutions=list_institutions)


# list institutions
@app.route("/institutions-list", methods=["GET"])
def institutions_list():
    institutions = institution.list_all()
    return render_template("institutions/institutions_list.html", institutions=institutions)

@app.route("/institutions-list-author-count", methods=["GET"])
def institutions_list_by_author_count():
    institutions = institution.list_all_by_author_count()
    return render_template("institutions/institutions_list.html", institutions=institutions)

# show or edit specific institution
@app.route("/institutions/<institution_id>", methods=["GET"])
def institution_details(institution_id: str):
    institution_details = institution.read(institution_id)
    template = "institutions/institution_details_view.html" if not request.args.get("edit") else "institutions/institution_details_form.html"
    return render_template(template, institution=institution_details, institution_id=institution_id)

# delete institution
@app.route("/institutions/<institution_id>", methods=["DELETE"])
def institution_delete(institution_id: str):
    try:
        print(f"Deleting institution {institution_id}")
        institution.delete(institution_id)
        response = make_response()
        response.headers["HX-Trigger"] = "refreshInstitutionList" # refresh the institution list
        return response
    except Exception as ex:
        r = make_response(render_template_string(f"{ex}"))
        return r

# search institutions
@app.route('/search-institutions', methods=['GET'])
def search_institutions():
    query = request.args.get('query', '').strip()  # Get the search term from the query parameter
    if query:
        institutions = institution.filterByName(query)
    else:
        institutions = institution.list_all()    
    return render_template('institutions/institutions_list.html', institutions=institutions)

# form to create new institution
@app.route("/institutions/new", methods=["GET"])
def new_institution_details():
    return render_template("institutions/institution_details_form.html")

@app.route("/institutions", methods=["POST"])
def save_institution_details():
    data = request.form
    institution_id = institution.generate_institution_id(data.get('Name'),data.get('Address')) # USE A HASH FUNCTION TO GENERATE A ID WITH 10 NUMBERS
    
    new_institution = institution.InstitutionForm(
        Name=data.get('Name'),
        Address=data.get('Address')
    )

    try:
        institution.create(institution_id, new_institution)
        response = make_response()
        print("NEW INSTITUTION ADDED")
        print(new_institution)
    except Exception as e:
        warning_message = str(e.args[1]).split("(50000)")[-2].split("]")[-1].strip() if len(e.args) > 1 else 'ERROR'
        response = make_response(render_template("institutions/institution_details_form.html", institution=new_institution, warning=warning_message))
        print(e)
        print("ERROR CREATING INSTITUTION")
        print(new_institution)

    response.headers["HX-Trigger"] = "refreshInstitutionList"
    return response

# update institution
@app.route("/institutions/<institution_id>", methods=["POST"])
def institution_update(institution_id: str):
    data = request.form

    new_institution = institution.InstitutionForm(
        Name=data.get('Name'),
        Address=data.get('Address')
    )
    
    try:
        institution.update(institution_id, new_institution)
        print("UPDATED INSTITUTION")
        response = make_response(institution_details(institution_id))
    except Exception as e:
        print("ERROR UPDATING INSTITUTION " + str(e.args[1]))
        print(new_institution)
        warning_message = str(e.args[1]).split("(50000)")[-2].split("]")[-1].strip() if len(e.args) > 1 else 'ERROR'
        response = make_response(render_template("institutions/institution_details_form.html", institution=new_institution, institution_id=institution_id, warning=warning_message))
    
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

# list authors
@app.route("/articles-list", methods=["GET"])
def articles_list():
    articles = article.list_all()
    return render_template("articles/articles_list.html", articles=articles)

def articles_list_by_author_count():
    articles = article.list_all_by_author_count()
    return render_template("articles/articles_list.html", articles=articles)

# show or edit specific article
@app.route("/articles/<article_id>", methods=["GET"])
def article_details(article_id: str):
    article_details = article.read(article_id)
    template = "articles/article_details_view.html" if not request.args.get("edit") else "articles/article_details_form.html"
    return render_template(template, article=article_details, article_id=article_id)

# delete article
@app.route("/articles/<article_id>", methods=["DELETE"])
def article_delete(article_id: str):
    try:
        print(f"Deleting article {article_id}")
        article.delete(article_id)
        response = make_response()
        response.headers["HX-Trigger"] = "refreshArticleList" # refresh the article list
        return response
    except Exception as ex:
        r = make_response(render_template_string(f"{ex}"))
        return r

# search articles
@app.route('/search-articles', methods=['GET'])
def search_articles():
    query = request.args.get('query', '').strip()  # Get the search term from the query parameter
    if query:
        articles = article.filterByName(query)
    else:
        articles = article.list_all()    
    return render_template('articles/articles_list.html', articles=articles)

# form to create new article
@app.route("/articles/new", methods=["GET"])
def new_article_details():
    return render_template("articles/article_details_form.html")

@app.route("/articles", methods=["POST"]) # publish new article
def save_article_details():
    data = request.form
    article_id = article.generate_article_id(data.get('Title'), data.get('Abstract'), data.get('DOI'), data.get('JournalName'), data.get('Volume'), data.get('StartPage'), data.get('EndPage')) # USE A HASH FUNCTION TO GENERATE A ID WITH 10 NUMBERS

    new_article = article.ArticleForm(
        Title=data.get('Title'),
        Abstract=data.get('Abstract'),
        DOI=data.get('DOI'),
        JournalName=data.get('JournalName'),
        Volume=data.get('Volume'),
        StartPage=data.get('StartPage'),
        EndPage=data.get('EndPage')
    )

    try:
        article.create(article_id, new_article)
        response = make_response()
        print("NEW ARTICLE ADDED")
        print(new_article)
    except Exception as e:
        warning_message = str(e.args[1]).split("(50000)")[-2].split("]")[-1].strip() if len(e.args) > 1 else 'ERROR'
        response = make_response(render_template("articles/article_details_form.html", article=new_article, warning=warning_message))
        print(e)
        print("ERROR CREATING ARTICLE")
        print(new_article)

    response.headers["HX-Trigger"] = "refreshArticleList"
    return response

# update article
@app.route("/articles/<article_id>", methods=["POST"])
def article_update(article_id: str):
    data = request.form

    new_article = article.ArticleForm(
        Title=data.get('Title'),
        Abstract=data.get('Abstract'),
        DOI=data.get('DOI'),
        JournalName=data.get('JournalName'),
        Volume=data.get('Volume'),
        StartPage=data.get('StartPage'),
        EndPage=data.get('EndPage')
    )

    try:
        article.update(article_id, new_article)
        print("UPDATED ARTICLE")
        response = make_response(article_details(article_id))
    except Exception as e:
        print("ERROR UPDATING ARTICLE " + str(e.args[1]))
        print(new_article)
        warning_message = str(e.args[1]).split("(50000)")[-2].split("]")[-1].strip() if len(e.args) > 1 else 'ERROR'
        response = make_response(render_template("articles/article_details_form.html", article=new_article, article_id=article_id, warning=warning_message))

    response.headers["HX-Trigger"] = "refreshArticleList"
    return response        

########

## Topics

@app.route("/topics")
def topics():
    list_topics = topic.list_all()
    return render_template("topics/topics.html", topics=list_topics)

# list topics
@app.route("/topics-list", methods=["GET"])
def topics_list():
    topics = topic.list_all()
    return render_template("topics/topics_list.html", topics=topics)

@app.route("/topics-list-article-count", methods=["GET"])
def topics_list_by_article_count():
    topics = topic.list_all_by_article_count()
    return render_template("topics/topics_list.html", topics=topics)

# show or edit specific topic
@app.route("/topics/<topic_id>", methods=["GET"])
def topics_details(topic_id: str):
    topic_details = topic.read(topic_id)
    template = "topics/topic_details_view.html" if not request.args.get("edit") else "topics/topic_details_form.html"
    return render_template(template, topic=topic_details, topic_id=topic_id)

# delete topic
@app.route("/topics/<topic_id>", methods=["DELETE"])
def topic_delete(topic_id: str):
    try:
        print(f"Deleting topic {topic_id}")
        topic.delete(topic_id)
        response = make_response()
        response.headers["HX-Trigger"] = "refreshTopicList" # refresh the topic list
        return response
    except Exception as ex:
        r = make_response(render_template_string(f"{ex}"))
        return r

# search topics
@app.route('/search-topics', methods=['GET'])
def search_topics():
    query = request.args.get('query', '').strip()  # Get the search term from the query parameter
    if query:
        topics = topic.filterByName(query)
    else:
        topics = topic.list_all()    

    return render_template('topics/topics_list.html', topics=topics)

# form to create new topic
@app.route("/topics/new", methods=["GET"])
def new_topic_details():
    return render_template("topics/topic_details_form.html")

@app.route("/topics", methods=["POST"]) # publish new topic
def save_topic_details():
    data = request.form
    topic_id = topic.generate_topic_id(data.get('Name'), data.get('Description')) # USE A HASH FUNCTION TO GENERATE A ID WITH 10 NUMBERS    

    new_topic = topic.TopicForm(
        Name=data.get('Name'),
        Description=data.get('Description')
    )

    try:
        topic.create(topic_id, new_topic)
        response = make_response()
        print("NEW TOPIC ADDED")
        print(new_topic)
    except Exception as e:
        warning_message = str(e.args[1]).split("(50000)")[-2].split("]")[-1].strip() if len(e.args) > 1 else 'ERROR'
        response = make_response(render_template("topics/topic_details_form.html", topic=new_topic, warning=warning_message))
        print(e)
        print("ERROR CREATING TOPIC")
        print(new_topic)

    response.headers["HX-Trigger"] = "refreshTopicList"
    return response

# update topic
@app.route("/topics/<topic_id>", methods=["POST"])
def topic_update(topic_id: str):
    data = request.form

    new_topic = topic.TopicForm(
        Name=data.get('Name'),
        Description=data.get('Description')
    )

    try:
        topic.update(topic_id, new_topic)
        print("UPDATED TOPIC")
        response = make_response(topics_details(topic_id))
    except Exception as e:
        print("ERROR UPDATING TOPIC " + str(e.args[1]))
        print(new_topic)
        warning_message = str(e.args[1]).split("(50000)")[-2].split("]")[-1].strip() if len(e.args) > 1 else 'ERROR'
        response = make_response(render_template("topics/topic_details_form.html", topic=new_topic, topic_id=topic_id, warning=warning_message))
    
    response.headers["HX-Trigger"] = "refreshTopicList"
    return response    

########

## Journals

@app.route("/journals")
def journals():
    list_journals = journal.list_all()
    return render_template("journals/journals.html", journals=list_journals)

# list journals
@app.route("/journals-list", methods=["GET"])
def journals_list():
    journals = journal.list_all()
    return render_template("journals/journals_list.html", journals=journals)

@app.route("/journals-list-article-count", methods=["GET"])
def journals_list_by_article_count():
    journals = journal.list_all_by_article_count()
    return render_template("journals/journals_list.html", journals=journals)

# show or edit specific journal
@app.route("/journals/<journal_id>", methods=["GET"])
def journal_details(journal_id: str):
    journal_details = journal.read(journal_id)
    template = "journals/journal_details_view.html" if not request.args.get("edit") else "journals/journal_details_form.html"
    return render_template(template, journal=journal_details, journal_id=journal_id)

# delete journal
@app.route("/journals/<journal_id>", methods=["DELETE"])
def journal_delete(journal_id: str):
    try:
        print(f"Deleting journal {journal_id}")
        journal.delete(journal_id)
        response = make_response()
        response.headers["HX-Trigger"] = "refreshJournalList" # refresh the journal list
        return response
    except Exception as ex:
        r = make_response(render_template_string(f"{ex}"))
        return r


# search journals
@app.route('/search-journals', methods=['GET'])
def search_journals():
    query = request.args.get('query', '').strip()   # Get the search term from the query parameter
    if query:
        journals = journal.filterByName(query)
    else:
        journals = journal.list_all()
    return render_template('journals/journals_list.html', journals=journals)

# form to create new journal
@app.route("/journals/new", methods=["GET"])
def new_journal_details():
    return render_template("journals/journal_details_form.html")

@app.route("/journals", methods=["POST"]) # publish new journal
def save_journal_details():
    data = request.form
    journal_id = journal.generate_journal_id(data.get('Name'), data.get('PrintISSN'), data.get('EletronicISSN'), data.get('Url'), data.get('Publisher'))

    new_journal = journal.JournalForm(
        Name=data.get('Name'),
        PrintISSN=data.get('PrintISSN'),
        EletronicISSN=data.get('EletronicISSN'),
        Url=data.get('Url'),
        Publisher=data.get('Publisher')
    )

    try:
        journal.create(journal_id, new_journal)
        response = make_response()
        print("NEW JOURNAL ADDED")
        print(new_journal)
    except Exception as e:
        warning_message = str(e.args[1]).split("(50000)")[-2].split("]")[-1].strip() if len(e.args) > 1 else 'ERROR'
        response = make_response(render_template("journals/journal_details_form.html", journal=new_journal, warning=warning_message))
        print(e)
        print("ERROR CREATING JOURNAL")
        print(new_journal)

    response.headers["HX-Trigger"] = "refreshJournalList"
    return response

# update journal
@app.route("/journals/<journal_id>", methods=["POST"])
def journal_update(journal_id: str):
    data = request.form

    new_journal = journal.JournalForm(
        Name=data.get('Name'),
        PrintISSN=data.get('PrintISSN'),
        EletronicISSN=data.get('EletronicISSN'),
        Url=data.get('Url'),
        Publisher=data.get('Publisher')
    )

    try:
        journal.update(journal_id, new_journal)
        print("UPDATED JOURNAL")
        response = make_response(journal_details(journal_id))
    except Exception as e:
        print("ERROR UPDATING JOURNAL " + str(e.args[1]))
        print(new_journal)
        warning_message = str(e.args[1]).split("(50000)")[-2].split("]")[-1].strip() if len(e.args) > 1 else 'ERROR'
        response = make_response(render_template("journals/journal_details_form.html", journal=new_journal, journal_id=journal_id, warning=warning_message))

    response.headers["HX-Trigger"] = "refreshJournalList"
    return response    


if __name__ == "__main__":
    app.run(debug=True, port=8080)
