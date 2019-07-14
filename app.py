import os
from bottle import (get, post, redirect, request, route, run, static_file, error, template)
import utils
import json
from collections import OrderedDict
from operator import itemgetter
from sys import argv


DEBUG = os.environ.get("DEBUG")
bottle.debug(False)


@route('/browse')
def browse():
    order_chosen = 'rating'
    series = [json.loads(utils.getJsonFromFile(series)) for series in utils.AVAILABE_SHOWS]
    if order_chosen == 'name':
        series_sorted = sorted(series, key=itemgetter('name'), reverse=False)
    elif order_chosen == 'rating':
        series_sorted = sorted(series, key=lambda show: float(show['rating']['average']), reverse=True)
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
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=section_template, sectionData={})


@route('/search', method = "POST")
def search_post():
    section_template = "./templates/search_result.tpl"
    query = request.forms.get("q")
    search_results = [json.loads(utils.getJsonFromFile(series)) for series in utils.AVAILABE_SHOWS]
    episodes = []
    for show in range(len(search_results)-1):
        for episode in range(len(search_results[show]['_embedded']['episodes'])-1):
            my_show = search_results[show]
            if query in str(my_show['name']) or query in str(my_show['_embedded']['episodes'][episode]['name']) or query in str(my_show['_embedded']['episodes'][episode]['summary']):
                newObj = {
                    "showid": search_results[show]["id"],
                    "episodeid": search_results[show]['_embedded']['episodes'][episode]["id"],
                    "text": search_results[show]['name'] + ": " + search_results[show]['_embedded']['episodes'][episode]['name'],
                    'rating': search_results[show]['rating']['average'],
                }
                episodes.append(newObj)
    for show in range(len(episodes)-1):
        print(episodes[show])
    sorted_results = sorted(episodes, key=lambda sortby: sortby['rating'])
    results = sorted_results
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=section_template,
    query = query, sectionData=results, results=results)


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


if DEBUG:
	bottle.run(host='localhost', port=7000)
else:
	bottle.run(host='0.0.0.0', port=argv[1])

