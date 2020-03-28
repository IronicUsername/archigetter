import json

from bs4 import BeautifulSoup
import cssutils
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()
origins = ['*']
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

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

        res['gifid'] = soup.find('div', {'id': 'gifid'}).text[1:]
        res['gifid_buffer'] = soup.find('img', {'id': 'buffer'})['index']
    else:
        res = {'message': 'something went wrong.', 'error': r.text}
    return res
