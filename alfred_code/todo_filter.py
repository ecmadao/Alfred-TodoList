# -*- coding: utf-8 -*-
import sys
import re
import alfred
from workflow import Workflow, Workflow3
from file import SPLIT, todo_files

reload(sys)
sys.setdefaultencoding('utf-8')


def todo_filter(wf):
	if len(wf.args):
		try:
			arg = re.findall(r'filter: (.*)', ''.join(wf.args))[0]
		except IndexError:
			arg = ''
	else:
		arg = ''
	
	file_object = todo_files(arg)
	file_items = file_object.files.items()
	
	todo_items = []
	
	for item in file_items:
		filename, file_obj = item
		for todo in file_obj['todos']:
			alfred_item = alfred.Item({'uid': 3, 'arg': '{filename}{split}{todo}'.format(filename=filename, split=SPLIT, todo=todo)}, todo, filename, ('new_todo.png', {'type': 'png'}))
			todo_items.append(alfred_item)

	alfred.write(alfred.xml(todo_items))
	wf.send_feedback()
	

if __name__ == '__main__':
	wf = Workflow3()
	logger = wf.logger
	sys.exit(wf.run(todo_filter))