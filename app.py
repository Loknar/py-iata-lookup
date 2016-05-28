#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2

import flask

import iata_scraper
import json_utils

app = flask.Flask(__name__)

POSITIVE = ('true', 'yes', '1')

def scrape_and_return_results(search_param, scraper):
	search_param_decoded = urllib2.unquote(search_param)
	pretty = (flask.request.args.get('pretty') in POSITIVE)
	results = {
		'results': scraper(search_param_decoded)
	}
	json_string = json_utils.dump_to_json(results, pretty)
	return flask.Response(
		response=json_string,
		status=200,
		mimetype='application/json'
	)

@app.route('/')
def index():
	return 'https://github.com/Loknar/py-iata-lookup#examples'

@app.route('/airline/code/<search_param>')
def airline_code(search_param):
	return scrape_and_return_results(
		search_param,
		iata_scraper.lookup_airline_by_code
	)

@app.route('/airline/name/<search_param>')
def airline_name(search_param):
	return scrape_and_return_results(
		search_param,
		iata_scraper.lookup_airline_by_name
	)

@app.route('/location/name/<search_param>')
def location_name(search_param):
	return scrape_and_return_results(
		search_param,
		iata_scraper.lookup_location_by_name
	)

@app.route('/location/code/<search_param>')
def location_code(search_param):
	return scrape_and_return_results(
		search_param,
		iata_scraper.lookup_location_by_code
	)

if __name__ == '__main__':
	app.run(
		'0.0.0.0',
		15000,
		use_reloader=True,
		use_debugger=True,
		processes=10
	)
