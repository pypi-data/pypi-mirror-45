#========================================================
#|            project          |  data-create |  Author |
#|  simplified file management |  23.04.2019  |  Gerod  |
#========================================================

##################################
#import the lib



###################################
#varibalse

name = "simplified file management" # name lib (project)
version = "23.04.2019 | Alpha 0.26" # verision lib (project)
author = "Gerod" # Author lib (project)
info = "functions:\n sifima.create(file)\n sifima.write(file, text)\n sifima.remove(file)\n sifima.read(file)" # Functions in lib (project)

###################################


###################################
#functions

def create(file): # create file user
	with open(file, "w") as files: # open file (w - write, but pass)
		pass # in function pass

def write(file, text): # write text in file user
	try:
		with open(file, "w") as files:
			files.write(text)
	except: # if error
		pass

def remove(file): # delete file user
	import os
	try:
		os.remove(file) # delete file in pc (name file = file)
	except: # if error
		pass

def read(file): # reaD file user
	try:
		with open(file, "r") as files:
			for text in files: # read full file
				text
			return text
	except: # if error
		pass

####################################