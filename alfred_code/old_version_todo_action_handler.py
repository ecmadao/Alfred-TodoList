# -*- coding: UTF-8 -*-
import sys
import re
import alfred
from workflow import Workflow
from file import SPLIT, todo_actions


reload(sys)
sys.setdefaultencoding('utf-8')


def todo_action_handler(wf):
	if len(wf.args):
		arg = ''.join(wf.args)
	else:
		arg = ''
		
	try:
		filename, todo, action = arg.split(SPLIT)
		actions_obj = todo_actions()

		if action:
			actions_obj.todo_actions()[action](filename, todo)
			sys.exit(0)
		else:
			todo_actions_list = []
			for actions in actions_obj.actions.items():
				action_name, action_icon = actions

				alfred_item = alfred.Item({'uid': alfred.uid(1), 'arg': '{filename}{split}{todo}{split}{action}'.format(filename=filename, split=SPLIT, todo=todo, action=action_name)}, action_name, '{action} this todo in todos/{filename}.md'.format(action=action_name, filename=filename), (action_icon, {'type': 'png'}))
				
				todo_actions_list.append(alfred_item)
			alfred.write(alfred.xml(todo_actions_list))	
	except ValueError:
		pass
	finally:
		wf.send_feedback()


if __name__ == '__main__':
	wf = Workflow()
	logger = wf.logger
	sys.exit(wf.run(todo_action_handler))