import os
from bottle import (get, post, redirect, request, route, run, static_file, error, template)
import utils
import json


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
def show_ajax(id):
    sectionTemplate = "./templates/show.tpl"
    my_data = json.loads(utils.getJsonFromFile(id))
    return template(sectionTemplate, result=my_data)


@route('/ajax/show/<id>/episode/<episodeid>')
def episode_ajax(id, episodeid):
    sectionTemplate = "./templates/episode.tpl"
    my_data = json.loads(utils.getJsonFromFile(id))
    episodes = my_data['_embedded']['episodes']
    for data in episodes:
        if data['id'] == int(episodeid):
            return template(sectionTemplate, result=data)


@route('/show/<id>/episode/<episodeid>')
def show(id, episodeid):
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
    my_data = [json.loads(utils.getJsonFromFile(series)) for series in utils.AVAILABE_SHOWS]
    episodes = []
    for episode in my_data[len(my_data)-1]['_embedded']['episodes']:
        episodes.append(episode)
        for data in episodes:
            print(search_name in data['summary'])  
            myresult = [] 
            if data['name'] == search_name or search_name in data['summary']: 
                newObj = {
                    # "showid": 'my_data["id"]',
                    # "episodeid": 'data["id"]',
                    # "text": "data['summary']"
                }
                print(my_data['id'])
                newObj['showid'] = my_data['id']
                newObj['episodeid'] = data['id']
                newObj['text'] = my_data['summary']
                myresult.append(newObj)  
                print(myresult)    
                return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                query = search_name, sectionData=myresult, results=myresult)



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
