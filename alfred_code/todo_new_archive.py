# -*- coding: UTF-8 -*-
import sys
import re
from file import create_new_archive, ARCHIVE_TITLE

reload(sys)
sys.setdefaultencoding('utf-8')


def new_archive(args):
	if len(args):
		arg = ''.join(args)
	else:
		arg = ''
		
	filename = re.findall(r'^{}(.+)$'.format(ARCHIVE_TITLE), arg)[0]
	if filename:
		create_new_archive(filename)
	sys.exit(0)
