import os
from bottle import (get, post, redirect, request, route, run, static_file, error, template)
import utils
import json
from collections import OrderedDict
from operator import itemgetter

@route('/browse')
def browse():
    order_chosen = 'rating'
    series = [json.loads(utils.getJsonFromFile(series)) for series in utils.AVAILABE_SHOWS]
    if order_chosen == 'name':
        series_sorted = sorted(series, key=itemgetter('name'), reverse=False)
    elif order_chosen == 'rating':
        series_sorted = sorted(series, key=lambda x: float(x['rating']['average']), reverse=True)
    else:
        series_sorted = sorted(series, key=itemgetter(order_chosen), reverse=False)
    section_template = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=section_template, sectionData=series_sorted)


@route('/show/<id_show>')
def show(id_show):
    if id_show not in utils.AVAILABE_SHOWS:
        section_template = "./templates/404.tpl"
        show = {}
    else:
        section_template = "./templates/show.tpl"
        show = json.loads(utils.getJsonFromFile(id_show))
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=section_template, sectionData = show)


@route('/ajax/show/<id_show>')
def show_ajax(id_show):
    section_template = "./templates/show.tpl"
    show = json.loads(utils.getJsonFromFile(id_show))
    return template(section_template, result=show)


@route('/ajax/show/<id_show>/episode/<id_episode>')
def episode_ajax(id_show, id_episode):
    section_template = "./templates/episode.tpl"
    show = json.loads(utils.getJsonFromFile(id_show))
    episodes = show['_embedded']['episodes']
    parsed_id_episode = int(id_episode)
    for chapter in episodes:
        if chapter['id'] == parsed_id_episode:
            return template(section_template, result=chapter)


@route('/show/<id_show>/episode/<id_episode>')
def episodes(id_show, id_episode):
    if id_show not in utils.AVAILABE_SHOWS:
        section_template = "./templates/404.tpl"
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=section_template,
                        sectionData={})
    show = json.loads(utils.getJsonFromFile(id_show))
    episodes = show['_embedded']['episodes']
    try:
        parsed_id_episode = int(id_episode)
        for chapter in episodes:
            if chapter['id'] == parsed_id_episode:
                section_template = "./templates/episode.tpl"
                return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=section_template,
                                sectionData=chapter)
    except ValueError:
        pass
    section_template = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=section_template, sectionData={})


@route('/search')
def search():
    section_template = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=section_template, sectionData = {})


@route('/search', method = "POST")
def search_post():
    section_template = "./templates/search_result.tpl"
    query = request.forms.get("q")
    my_data = [json.loads(utils.getJsonFromFile(series)) for series in utils.AVAILABE_SHOWS]
    episodes = []
    for x in range(len(my_data)-1):
        for i in range(len(my_data[x]['_embedded']['episodes'])-1):
            print(i)
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
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=section_template,
    query = query, sectionData=myData, results=myData)


@error(404)
def not_found(error):
    section_template = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=section_template, sectionData = {})


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
    section_template = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=section_template, sectionData = {})


run(host='localhost', port=os.environ.get('PORT', 7050))
