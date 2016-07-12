# -*- coding: UTF-8 -*-
import sys
import re
from todos_files.files_helper import create_new_archive
from const_value import ARCHIVE_TITLE

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
