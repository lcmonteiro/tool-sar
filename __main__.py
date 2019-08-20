#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from argparse   import ArgumentParser
from CheckUUIDS import main as check_uuids
# -------------------------------------------------------------------------------------------------
# parsers
# -------------------------------------------------------------------------------------------------
# head
# -----------------------------------------------------------------------------
head = ArgumentParser(prog='toolsar')
sub  = head.add_subparsers()
# -----------------------------------------------------------------------------
# check uuid
# -----------------------------------------------------------------------------
parser = sub.add_parser('check-uuids')
# arguments
parser.add_argument('path', type=str, help='search path')
# function
parser.set_defaults(func=check_uuids)
# -------------------------------------------------------------------------------------------------
# execute
# -------------------------------------------------------------------------------------------------
from colorlog import basicConfig as config_logger
from logging  import INFO
from sys      import stdout

if __name__ == '__main__':
	# logger configuration
	config_logger(
		format = '%(log_color)s%(asctime)s %(levelname)-8s %(reset)s| %(message)s',
		stream = stdout,
		level  = INFO,
		datefmt='%H:%M:%S')
	# call method
	opt = head.parse_args()
	opt.func(opt)
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------