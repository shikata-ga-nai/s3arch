#!/usr/bin/env python3
import urllib.parse
import sys
from lib.search import *
from lib.core.Controller import Controller
from lib.core.ArgumentsParser import ArgumentsParser


class Program:
	def __init__(self):
		self.arguments = ArgumentsParser()

	def run(self):
		self.controller = Controller(self.arguments)
	

if __name__ == '__main__':
    print("s3arch v0.1")
    main = Program()
    main.run()
	
