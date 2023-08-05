#!/usr/bin/python3
#    QASDAD, the quick and simple data analysis and documentation program
#    Copyright (C) 2018 Volker Weißmann . Contact: volker.weissmann@gmx.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import shutil
import sys
import re
if len(sys.argv) != 2:
	print("usuage: python3 qasdad.py source")
	exit(7001)
SOURCE_PATH = sys.argv[1]
if not os.path.isfile(SOURCE_PATH) and not os.path.isdir(SOURCE_PATH):
	print("source does not exist")
	exit(7002)
sps = list(os.path.split(SOURCE_PATH))
if sps[-1] == "": #This if is neccessary because the user can run qasdad.py dirA/ dirB or qasdad.py dirA dirB
	sps = sps[:-1]
sps[-1] += "_qasdad_output"
OUT_PATH=os.path.join(*sps)
try:
	shutil.rmtree(OUT_PATH)
except:
	pass
os.makedirs(OUT_PATH)
DATA_PATH = os.path.join(OUT_PATH, "qasdad_out")
os.makedirs(DATA_PATH)
extracted = {}
def readFile(sourcepath, latexout):
	source = open(sourcepath, "r")
	latexFile = open(latexout, "w")
	lineNum = 0
	num = None
	for line in source:
		lineNum += 1
		if num is None and line.startswith("\\iffalse BEGIN QASDAD"):
			try:
				num = int(line[21:])
			except:
				print("aborting: unable to parse this line:", line)
				exit(7003)
			if num in extracted:
				print("aborting: multiple sections with the number", num)
				exit(7003)
			path = os.path.join(DATA_PATH,str(num) + ".tex")
			#extracted[num] = "setTexFile(open(\"" + path + "\",'w'))\nsetLatexPath(\"" + latexout + "\")\n" #TODO muss man hier die " in path und in latexout scapen?
			extracted[num] = "qasdad._TEX_FILE_ = open(\"" + path + "\",'w')\n_LATEX_PATH_=\"" + latexout + "\"\n" #TODO muss man hier die " in path und in latexout scapen?
			path = os.path.relpath(path,start=os.path.dirname(latexout))
			latexFile.write("\\input{" + path + "}\n")
			continue
		elif num is not None and line.startswith("\\iffalse BEGIN QASDAD"):
			print("aborting: unexpected line ", line)
			exit(7003)
		elif num is not None and line.startswith("END QASDAD \\fi"):
			num = None
			continue
		elif num is None and line.startswith("END QASDAD \\fi"):
			print("aborting: unexpected line ", line)
			exit(7003)
		if num is None:
			latexFile.write(line)
		else:
			extracted[num] += line
if os.path.isfile(SOURCE_PATH):
	readFile(SOURCE_PATH, os.path.join(OUT_PATH,os.path.basename(SOURCE_PATH)))
elif os.path.isdir(SOURCE_PATH):
	for subdir, dirs, files in os.walk(SOURCE_PATH):
		for file in files:
			if(file.endswith(".tex")):
				sourcepath = os.path.join(subdir, file)
				rel = os.path.relpath(sourcepath,start=SOURCE_PATH)
				latexout = os.path.join(OUT_PATH,rel)
				readFile(sourcepath,latexout)
else:
	print("the first argument:", SOURCE_PATH, "is neither a file nor a directory") #Dieser Fall wird eigentlich schon oben abgefangen
	exit(7002)

def filesInOneFile(outfile, infiles):
	shutil.copy2(infiles[0], outfile)
	for i in range(1, len(infiles)):
		outf = open(outfile, "a")
		inf = open(infiles[i], "r")
		for line in inf:
			outf.write(line)
		outf.close()

#filesInOneFile(os.path.join(DATA_PATH, "python.py"),[
#	os.path.join(os.path.dirname(__file__), "qasdadEnv","imports.py"),
#        os.path.join(os.path.dirname(__file__), "qasdadEnv","constants.py"),
#        os.path.join(os.path.dirname(__file__), "qasdadEnv","units.py"),
#        os.path.join(os.path.dirname(__file__), "qasdadEnv","equation.py"),
#        os.path.join(os.path.dirname(__file__), "qasdadEnv","table.py"),
#        os.path.join(os.path.dirname(__file__), "qasdadEnv","plot.py"),
#	os.path.join(os.path.dirname(__file__), "qasdadEnv","main.py"),
#	os.path.join(os.path.dirname(__file__), "qasdadEnv","calcColumn.py")])

pythonPath = os.path.join(DATA_PATH, "python.py")
pythonFile = open(pythonPath, "w")
#pythonFile.write("from qasdad import *\nsetDataPath(\"" + DATA_PATH + "\")\n") #TODO muss man nicht " in DATA_PATH escapen?
pythonFile.write("from qasdad import *\nimport qasdad\n_DATA_PATH_=\"" + DATA_PATH + "\"\n") #TODO muss man nicht " in DATA_PATH escapen?

for key in sorted(extracted.keys()):
	pythonFile.write(extracted[key])
pythonFile.close()
print("running the python script...")
ret = os.system("python3 \"" + pythonPath.replace("\"", "\\\"")  + "\"")
if ret != 0:
	print("error in python.py") 
	exit(ret)#TODO was ist wenn ret zwischen 7000 und 7999 liegt
#os.system("pdflatex -output-directory " + DATA_PATH + " " + DATA_PATH + "/latex.tex > /dev/null")
#if not nopdflatex:
#	print("running pdflatex...")
#	#ret = os.system("pdflatex --interaction=scrollmode -output-directory " + DATA_PATH + " " + DATA_PATH + "/latex.tex > " + DATA_PATH + "/latexstdout.txt" )
#	ret = os.system("pdflatex -output-directory " + DATA_PATH + "/tex " + DATA_PATH + "/tex/latex.tex" ) #--interaction=scrollmode
#	if ret != 0:
#		file = open(DATA_PATH + "/latexstdout.txt" ) 
#		for line in file:
#			print(line, end='')
#			print("error in latex.tex")
#			exit(ret)
#	os.system("pdflatex --interaction=scrollmode -output-directory " + DATA_PATH + "/tex " + DATA_PATH + "/tex/latex.tex" ) #TODO nur doppelt kompilieren wenn es benötigt wird
#	os.rename(DATA_PATH + "/tex/latex.aux", DATA_PATH + "/latex.aux")
#	os.rename(DATA_PATH + "/tex/latex.log", DATA_PATH + "/latex.log")
#	os.rename(DATA_PATH + "/tex/latex.pdf", os.path.splitext(SOURCEFILE_PATH)[0] + ".pdf")
#	print("pdflatex -output-directory " + DATA_PATH + "/tex " + DATA_PATH + "/tex/latex.tex")
