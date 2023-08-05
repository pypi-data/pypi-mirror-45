#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##

from lutin import debug
from lutin import system
from lutin import tools
from lutin import env
import os

class System(system.System):
	def __init__(self, target):
		system.System.__init__(self)
		# create some HELP:
		self.set_help("OpenGL: Generic graphic library")
		self.set_valid(True)
		# no check needed ==> just add this:
		self.add_depend([
		    'khr',
		    ])
		self.add_flag('link-lib', 'EGL')
		if env.get_isolate_system() == True:
			self.add_header_file([
			    "/usr/include/EGL/*"
			    ],
			    destination_path="EGL",
			    recursive=True)
	


