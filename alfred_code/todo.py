# -*- coding: UTF-8 -*-
import sys
import re
import alfred
from workflow import Workflow
from file import read_files, SPLIT, FILES


def filter_items(arg):
	def filter_fun(item):
		re_result = re.search(r'{}'.format(arg), item)
		result = True if re_result else False
		return result
	return filter_fun


def todo(wf):
	if len(wf.args):
		arg = ''.join(wf.args)
	else:
		arg = ''
	
	filter_fun = filter_items(arg)
	all_items = read_files()
	
	todo_items = []
	for item in all_items.items():
		filename, todos = item
		for todo in filter(filter_fun, todos):
			alfred_item = alfred.Item({'uid': 3, 'arg': '{filename}{split}{todo}{split}'.format(filename=filename, split=SPLIT, todo=todo)}, todo, filename, ('new_todo.png', {'type': 'png'}))
			todo_items.append(alfred_item)
	
	if len(todo_items) == 0:
		for filename in FILES:
			alfred_item = alfred.Item({'uid': 3, 'arg': '{filename}{split}{todo}{split}add'.format(filename=filename, split=SPLIT, todo=arg)}, filename, 'add new todo in todos/{}.md'.format(filename), ('new_todo.png', {'type': 'png'}))
			todo_items.append(alfred_item)

	alfred.write(alfred.xml(todo_items))
	wf.send_feedback()
	

if __name__ == '__main__':
	wf = Workflow()
	logger = wf.logger
	sys.exit(wf.run(todo))