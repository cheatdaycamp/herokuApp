import os
from bottle import (get, post, redirect, request, route, run, static_file, error, template)
import utils
import json


# Static Routes

@route('/show/7')
def show():
    print("dsaads")
    sectionTemplate = "./templates/show.tpl"
    my_data = [json.loads(utils.getJsonFromFile(id))]
    print(my_data)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {my_data})


@route('/browse')
def browse_series():
    sectionTemplate = "./templates/browse.tpl"
    my_data = [json.loads(utils.getJsonFromFile(series)) for series in utils.AVAILABE_SHOWS]
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=my_data)


@route('/show/<id>')
def show(id):
    sectionTemplate = "./templates/show.tpl"
    my_data = json.loads(utils.getJsonFromFile(id))
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = my_data)


@route('/ajax/show/<id>')
def show(id):
    sectionTemplate = "./templates/show.tpl"
    my_data = json.loads(utils.getJsonFromFile(id))
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = my_data)


# correct thsi for the episodes
@route('/ajax/show/<id>/episode/<episodeid>')
def show(id, episodeid):
    print(episodeid)
    sectionTemplate = "./templates/episode.tpl"
    my_data = json.loads(utils.getJsonFromFile(id))
    episodes = my_data['_embedded']['episodes']
    for data in episodes:
        print(data["id"], episodeid)
        if data['id'] == int(episodeid):
            return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=data)


@route('/show/<id>/episode/<episodeid>')
def show(id, episodeid):
    print(id)
    sectionTemplate = "./templates/episode.tpl"
    my_data = [json.loads(utils.getJsonFromFile(series)) for series in utils.AVAILABE_SHOWS]
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=my_data)


@route('/search')
def index():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})


@route('/search', method = "POST")
def search():
    sectionTemplate = "./templates/search_result.tpl"
    search_name = request.forms.get("q")
    my_data = json.loads(utils.getJsonFromFile(7))
    episodes = my_data['_embedded']['episodes']
    for data in episodes:
        print(search_name in data['summary'])  
        if data['name'] == search_name or search_name in data['summary']:      
            return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
            query = search_name, sectionData=data, results=data)



@error(404)
def not_found(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})


@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")


@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})


run(host='localhost', port=os.environ.get('PORT', 7050))





    # with open("./data/7.json", "r") as myfile:
    #     data=myfile.read()
    # obj = json.loads(data)
    # print("id: " + str(obj['id']))
    # return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})