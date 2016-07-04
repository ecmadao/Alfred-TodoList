# -*- coding: utf-8 -*-
import sys
import re
import alfred
from workflow import Workflow, Workflow3
from file import SPLIT, todo_files

reload(sys)
sys.setdefaultencoding('utf-8')


def todo(wf):
	if len(wf.args):
		arg = ''.join(wf.args)
	else:
		arg = ''
	
	file_object = todo_files(arg)
	file_items = file_object.files.items()
	
	todo_items = []
	
	for item in file_items:
		filename, file_obj = item
		for todo in file_obj['todos']:
			alfred_item = alfred.Item({'uid': 3, 'arg': '{filename}{split}{todo}{split}'.format(filename=filename, split=SPLIT, todo=todo)}, todo, filename, ('new_todo.png', {'type': 'png'}))
			todo_items.append(alfred_item)
	
	if len(todo_items) == 0:
	
		for file_tuple in file_items:
			filename, file_obj = file_tuple
			file_icon = file_obj['icon']
			alfred_item = alfred.Item({'uid': 3, 'arg': '{filename}{split}{todo}{split}add'.format(filename=filename, split=SPLIT, todo=arg)}, filename, 'add new todo in todos/{}.md'.format(filename), (file_icon, {'type': 'png'}))
			todo_items.append(alfred_item)

	alfred.write(alfred.xml(todo_items))
	wf.send_feedback()
	

if __name__ == '__main__':
	wf = Workflow3()
	logger = wf.logger
	sys.exit(wf.run(todo))