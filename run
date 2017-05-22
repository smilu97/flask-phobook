#!/usr/bin/env python

from app import app
import sys

if __name__ == '__main__':
	try:
		config = {}
		if len(sys.argv) < 2:
			raise Exception('./run.py <port>')
		config['port'] = int(sys.argv[1])
		app.run(**config)
	except Exception as e:
		print e