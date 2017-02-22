#!/usr/bin/env python

import re
import os
import time
import json
import logging

from textblob import TextBlob
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

cache = {}
cache_primed = False
cache_filename = os.getenv("CACHE_LOCATION", "./_cache/cache")


def add_to_cache(text, sent):
    global cache
    with open(cache_filename, 'w+') as cache_backing:
        cache[text] = sent
        json.dump(cache, cache_backing)


def flush_cache():
    global cache
    with open(cache_filename, 'w+') as cache_backing:
        cache = {}
        json.dump(cache, cache_backing)


def prime_cache():
    global cache_primed
    global cache
    if not cache_primed and os.path.exists(cache_filename):
        with open(cache_filename, 'r+') as cache_backing:
            cache = json.load(cache_backing)
            cache_primed = True
            print "Cache primed to {}".format(cache)


def clean_input(text):
    '''
    http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
    '''
    return ' '.join(re.sub(
                "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",
                " ", text).split())


def get_sentiment(text):
    prime_cache()

    ret = {}
    if text in cache:
        ret = cache[text]
        ret["cache_hit"] = True

    tb = TextBlob(text)

    polarity = tb.sentiment.polarity
    ret["polarity"] = polarity
    if polarity > 0:
        ret["analysis"] = "positive"
    elif polarity == 0:
        ret["analysis"] = "neutral"
    elif polarity < 0:
        ret["analysis"] = "negative"
    else:
        raise "Unacceptable polarity"

    add_to_cache(text, ret)
    return ret


@app.route('/', methods=["POST"])
def do_anal():
    if request.form["text"]:
        sent = get_sentiment(clean_input(request.form["text"]))
        sent["timestamp"] = time.time()
        sent["text"] = request.form["text"]

        ret = json.dumps(sent)

    else:
        ret = json.dumps({"error": "no input"})

    r = make_response(ret)
    r.mimetype = 'application/json'
    return r


@app.route('/list')
def list_cache():
    r = make_response(json.dumps(cache.keys()))
    r.mimetype = 'application/json'
    return r


@app.route('/flush')
def flush():
    flush_cache()
    return list_cache()

if __name__ == '__main__':
    t = raw_input()
    print clean_input(t)
    print get_sentiment(clean_input(t))
