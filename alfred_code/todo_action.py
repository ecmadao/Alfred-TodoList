# -*- coding: UTF-8 -*-
import sys
from file import SPLIT, todo_actions

reload(sys)
sys.setdefaultencoding('utf-8')


def todo_action(args):
	if len(args):
		arg = ''.join(args)
	else:
		arg = ''
		
	try:
		filename, todo, action = arg.split(SPLIT)
		actions_obj = todo_actions()
		
		if action:
			actions_obj.todo_actions[action](filename, todo)
	except ValueError:
		pass
	finally:
		sys.exit(0)
