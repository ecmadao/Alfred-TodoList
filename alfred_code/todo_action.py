# -*- coding: UTF-8 -*-
import sys
from workflow import Workflow
from file import SPLIT, todo_actions

reload(sys)
sys.setdefaultencoding('utf-8')


def todo_action(wf):
	if len(wf.args):
		arg = ''.join(wf.args)
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
		wf.send_feedback()


if __name__ == '__main__':
	wf = Workflow()
	logger = wf.logger
	sys.exit(wf.run(todo_action))
