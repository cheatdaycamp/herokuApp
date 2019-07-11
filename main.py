import os
from bottle import (get, post, redirect, request, route, run, static_file, error, template)
import utils
import json

# Static Routes


@route('/browse')
def browse():
    sectionTemplate = "./templates/browse.tpl"
    my_data = [json.loads(utils.getJsonFromFile('7')), json.loads(utils.getJsonFromFile('66'))]
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = my_data)

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
