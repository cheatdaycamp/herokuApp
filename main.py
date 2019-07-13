import os
from bottle import (get, post, redirect, request, route, run, static_file, error, template)
import utils
import json
from collections import OrderedDict

@route('/browse')
def browse():
    sectionTemplate = "./templates/browse.tpl"
    series = [json.loads(utils.getJsonFromFile(series)) for series in utils.AVAILABE_SHOWS]
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=series)


@route('/show/<id_show>')
def show(id_show):
    sectionTemplate = "./templates/show.tpl"
    show = json.loads(utils.getJsonFromFile(id_show))
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = show)


@route('/ajax/show/<id_show>')
def show_ajax(id_show):
    sectionTemplate = "./templates/show.tpl"
    show = json.loads(utils.getJsonFromFile(id_show))
    return template(sectionTemplate, result=show)


@route('/ajax/show/<id_show>/episode/<id_episode>')
def episode_ajax(id_show, id_episode):
    sectionTemplate = "./templates/episode.tpl"
    show = json.loads(utils.getJsonFromFile(id_show))
    episodes = show['_embedded']['episodes']
    for chapter in episodes:
        if chapter['id'] == int(id_episode):
            return template(sectionTemplate, result=chapter)


@route('/show/<id_show>/episode/<id_episode>')
def show(id_show, id_episode):
    sectionTemplate = "./templates/episode.tpl"
    episode = [json.loads(utils.getJsonFromFile(series)) for series in utils.AVAILABE_SHOWS]
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData=episode)


@route('/search')
def index():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})


@route('/search', method = "POST")
def search():
    sectionTemplate = "./templates/search_result.tpl"
    query = request.forms.get("q")
    my_data = [json.loads(utils.getJsonFromFile(series)) for series in utils.AVAILABE_SHOWS]
    episodes = []
    for x in range(len(my_data)-1):
        for i in range(len(my_data[x]['_embedded']['episodes'])-1):
            my_show = my_data[x]
            if query in str(my_show['name']) or query in str(my_show['_embedded']['episodes'][i]['name']) or query in str(my_show['_embedded']['episodes'][i]['summary']):     
                newObj = {
                    "showid": my_data[x]["id"],
                    "episodeid": my_data[x]['_embedded']['episodes'][i]["id"],
                    "text": my_data[x]['name'] + ": " + my_data[x]['_embedded']['episodes'][i]['name'],
                    'rating': my_data[x]['rating']['average'],
                }
                episodes.append(newObj)
    for x in range(len(episodes)-1):
        print(episodes[x])
    newlist = sorted(episodes, key=lambda k: k['rating'])

    myData = newlist  
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
    query = query, sectionData=myData, results=myData)



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
