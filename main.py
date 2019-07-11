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


@route('/search')
def index():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})


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