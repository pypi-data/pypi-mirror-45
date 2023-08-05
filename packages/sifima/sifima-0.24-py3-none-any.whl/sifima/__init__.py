name = "simplified file management"
version = "17.04.2019 | Alpha 0.24"
author = "Gerod"
info = "functions:\n sifima.create(file)\n sifima.write(file, text)\n sifima.remove(file)\n sifima.read(file)"

def __FileNotFoundErro(file):
	print("(ErrorSiFiMa) NotFoundFile: {}".format(file))

def create(file):
	with open(file, "w") as files:
		pass

def write(file, text):
	try:
		with open(file, "w") as files:
			files.write(text)
	except FileNotFoundError:
		__FileNotFoundError(file)

def remove(file):
	import os
	try:
		os.remove(file)
	except FileNotFoundError:
		__FileNotFoundError(file)

def read(file):
	try:
		with open(file, "r") as files:
			for text in files:
				text
			return text
	except FileNotFoundError:
		__FileNotFoundError(file)