#!*~*encoding:utf-8*~*

from __future__ import print_function
import os
import sys
from make_colors import make_colors
from pydebugger.debug import debug
import re
import cmdw
max_width = cmdw.getWidth()

class torrent_rename(object):
	def __init__(self):
		super(torrent_rename, self)

	def getName(self, torrent_file, overwrite="auto"):
		output = ''
		with open(torrent_file, 'rb') as tf:
			output = tf.read()
		tf.close()

		if output:
			# name = re.findall()
			name = re.findall(b'(name\d+:)(.*?)(\d+:)', output)
			print (make_colors("NAME  :", 'black', 'lightgreen'), name)
			debug(name=name)
			if len(name[0]) > 2:
				name = name[0][1]
			print (make_colors("NAME  :", 'black', 'lightyellow'), name)
			# print "RENAME:", name + ".torrent"
			dst = os.path.join(os.path.dirname(os.path.abspath(torrent_file)), str(name))  + ".torrent"
			count = 1
			overwrite_string = ""
			if os.path.isfile(dst):
				if not os.stat(dst).st_size == os.stat(os.path.abspath(torrent_file)).st_size:
					if overwrite == "auto":
						if len(re.findall(b"_\d+\.torrent", os.path.basename(dst))) > 0:
							count = int(re.findall(b"_\d+", os.path.basename(dst)[1:])) + 1
						dst = os.path.join(os.path.dirname(os.path.abspath(torrent_file)), str(name))  + "_" + str(count) + ".torrent"
						overwrite_string = " " + make_colors("[OVERWRITE]", 'lightwhite', 'lightred')
					elif isinstance(overwrite, bool):
						if overwrite:
							os.remove(dst)
							overwrite_string = " " + make_colors("[OVERWRITE]", 'lightwhite', 'lightred')
					print (make_colors("RENAME", 'lightwhite', 'lightblue') + "%s:"%(overwrite_string), name + ".torrent")
					os.rename(os.path.abspath(torrent_file), dst)
				else:
					print (make_colors("RENAME", 'lightwhite', 'lightblue') + ": " + make_colors("[PASS]", 'lightwhite', 'lightmagenta') + " " +  name + ".torrent")
			else:
				print (make_colors("RENAME", 'lightwhite', 'lightblue') + "%s:"%(overwrite_string), name + ".torrent")
				os.rename(os.path.abspath(torrent_file), dst)
			print ("-"*max_width)
			# re.findall('(name\d+:)(.*?)(\d+:)', data)
			# re.findall(r"(pizza|hot)\s*(.*?)\s*(?!\1)(?:hot|pizza)",x)]

	def rename(self, path, overwrite="auto"):
		if os.path.isdir(os.path.abspath(path)):
			debug("IS_DIR")
			# listdir_1 = os.popen("dir /b " + path).readlines()
			listdir_1 = os.listdir(path)
			# print "listdir_1 =", listdir_1
			# debug(listdir_1=listdir_1)
			listdir = []
			for i in listdir_1:
				dst = os.path.join(path, i.split("\n")[0])
				if os.path.isfile(dst):
					listdir.append(dst)
			debug(listdir=listdir)
			# print "listdir =", listdir
			for i in listdir:
				print (make_colors("FILE  :", 'black', 'lightcyan') + i)
				self.getName(i, overwrite)
		elif os.path.isfile(os.path.abspath(path)):
			print (make_colors("FILE  :", 'black', 'lightcyan') + path)
			self.getName(path, overwrite)
		else:
			self.usage(print_help=True)

	def usage(self, print_help=False):
		import argparse
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument("PATH", help="torrent file or directory containts torrent files", action='store')
		parser.add_argument('-o', '--overwrite', help='overwrite action: [1,auto], auto: auto rename, default:auto', action='store', default="auto")
		if len(sys.argv) == 1:
			parser.print_help()
		elif print_help:
			parser.print_help()
		else:
			args = parser.parse_args()
			if args.overwrite == '1':
				overwrite = True
			if args.overwrite == 'auto':
				overwrite = 'auto'
			self.rename(args.PATH, overwrite)

if __name__ == '__main__':
	c = torrent_rename()
	# c.getName(sys.argv[1])
	# c.rename(sys.argv[1])
	c.usage()