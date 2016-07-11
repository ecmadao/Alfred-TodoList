# -*- coding: UTF-8 -*-
import sys
from todos_files import todo_files
from const_value import SPLIT

reload(sys)
sys.setdefaultencoding('utf-8')


def todo_action(args):
	if len(args):
		arg = ''.join(args)
	else:
		arg = ''

	try:
		filename, todo, action = arg.split(const_value.SPLIT)
		actions_obj = todo_files()

		if action:
			actions_obj.todo_actions[action](filename, todo)
	except ValueError:
		pass
	finally:
		sys.exit(0)
