#!/usr/bin/env python2

import vping
import sys

def usage():
	if len(sys.argv) == 1:
		print "\n"
		print("USAGE: HOST TIMEOUT[2] COUNT[4]")
	else:
		HOST = None
		TIMEOUT = 2
		COUNT = 4

		if len(sys.argv) == 2:
			HOST = sys.argv[1]
		elif len(sys.argv) == 3:
			HOST = sys.argv[1]
			TIMEOUT = sys.argv[2]
		elif len(sys.argv) == 4:
			HOST = sys.argv[1]
			TIMEOUT = sys.argv[2]
			COUNT = sys.argv[3]
		else:
			print("USAGE: HOST TIMEOUT COUNT")

		vping.verbose_ping(HOST, int(TIMEOUT), int(COUNT))

if __name__ == '__main__':
	usage()

