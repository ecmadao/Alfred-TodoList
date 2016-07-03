# -*- coding: UTF-8 -*-
import sys
import re
import alfred
from workflow import Workflow
from file import todo_actions, SPLIT, ACTIONS


def todo_action_handler(wf):
	if len(wf.args):
		arg = ''.join(wf.args)
	else:
		arg = ''
		
	filename, todo, action = arg.split(SPLIT)

	if action:
		todo_actions()[action](filename, todo)
		sys.exit(0)
	else:
		todo_actions_list = []
		for action in ACTIONS:
			alfred_item = alfred.Item({'uid': 4, 'arg': '{filename}{split}{todo}{split}{action}'.format(filename=filename, split=SPLIT, todo=todo, action=action)}, action, '{action} this todo in todos/{filename}.md'.format(action=action, filename=filename), ('new_todo.png', {'type': 'png'}))
			todo_actions_list.append(alfred_item)
		alfred.write(alfred.xml(todo_actions_list))	
	wf.send_feedback()


if __name__ == '__main__':
	wf = Workflow(capture_args=True)
	logger = wf.logger
	sys.exit(wf.run(todo_action_handler))