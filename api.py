from bs4 import BeautifulSoup
import cssutils
from fastapi import FastAPI
import requests

app = FastAPI()
checklist = [['div', 'screenbg', 'style'], ['div', 'screenfg', 'style'], ['img', 'buffer', 'src']]


@app.get('/')
def root():
    return {'message': 'Hey.'}


@app.get('/getTV')
def getTV():
    r = requests.get(url='https://archillect.com/tv')
    soup = BeautifulSoup(r.text, 'html.parser')

    res = {}
    if r.status_code == 200:
        for ids in checklist:
            elem = soup.find(ids[0], {'id': ids[1]})[ids[2]]
            elem_src = (cssutils.parseStyle(elem)['background-image'][4:-1] if ids[2] != 'src' else elem)
            res[ids[1]] = elem_src
    else:
        res = {'message': 'something went wrong.'}
    return res
