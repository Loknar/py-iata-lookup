#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

def bytify(input):
	'''
	Helper function to save utf-8 texts to json without the escape sequences.
	http://stackoverflow.com/q/18337407
	'''
	if isinstance(input, dict):
		return {bytify(key): bytify(value)
			for key, value in input.iteritems()}
	elif isinstance(input, list):
		return [bytify(element) for element in input]
	elif isinstance(input, unicode):
		return input.encode('utf-8')
	elif isinstance(input, str):
		return unicode(input).encode('utf-8')
	else:
		return input

def dump_to_json(data, pretty=False):
	'''
	Dumps a python dict data object to json string.
	'''
	bytified_data = bytify(data)
	if pretty:
		data_text = json.dumps(
			bytified_data,
			indent=4,
			ensure_ascii=False,
			sort_keys=True
		)
	else:
		data_text = json.dumps(
			bytified_data,
			separators=(',', ':'),
			ensure_ascii=False,
			sort_keys=True
		)
	return data_text
