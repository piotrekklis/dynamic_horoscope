from flask import Flask, request, render_template, jsonify
from models import db, Horoscope
import psycopg2
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import atexit
from apscheduler.scheduler import Scheduler
from random import randint

app = Flask(__name__)

POSTGRES = {
    'user': 'your_db_username',
    'pw': 'your_db_password',
    'db': 'your_db_name',
    'host': 'your_db_host',
    'port': 'your_db_port',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

cron = Scheduler(daemon=True)
cron.start()

@cron.interval_schedule(hours=24)
def job_function():
    with app.app_context():
        signs = ['koziorozec', 'wodnik', 'ryby', 'baran', 'byk', 'bliznieta', 'rak', 'lew', 'panna', 'waga', 'skorpion', 'strzelec']

        for i in signs:

            page = requests.get('https://horoskop.wp.pl/horoskop/horoskop-dzienny/' + i)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id='artykul_srodek')

            elems = results.find_all('p')
            horoscope = elems[0].text

            random_horoscope_list = horoscope.split('.')

            for r in random_horoscope_list:
                if r.strip() != '':
                    a = r.strip()
                    sentence = a.capitalize() + '.'
                    result = Horoscope(sentence, i, datetime.now())
                    db.session.add(result)
                    db.session.commit()
        
    return 'OK'

@app.route('/horoscope')
def get_horoscope():
    sign = request.args['sign']
    counter = 0
    corpus = []
    horoscope_texts = Horoscope.query.filter_by(sign=sign).all()
    while counter < 5:
        temp_sentence = horoscope_texts[randint(0, len(horoscope_texts)-1)]
        if temp_sentence.text not in corpus:
            corpus.append(temp_sentence.text)
            counter = counter + 1
        else:
            pass

    for i in corpus:
        print(i)

    return jsonify({'corpus': corpus})

@app.route('/')
def index():
    signs_list = []
    all_signs = Horoscope.query.all()
    for i in all_signs:
        if i.sign not in signs_list:
            signs_list.append(i.sign)
    
    return render_template('index.html', signs=signs_list)

atexit.register(lambda: cron.shutdown(wait=False))

if __name__ == '__main__':
    app.run()