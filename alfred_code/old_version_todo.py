# -*- coding: utf-8 -*-
import sys
from workflow import Workflow3
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
	
	todo_items = 0
	
	for item in file_items:
		filename, file_obj = item
		todo_items += len(file_obj['todos'])
		for todo in file_obj['todos']:
			
			wf.add_item(title=todo, 
						subtitle=filename, 
						arg='{filename}{split}{todo}{split}'.format(filename=filename, split=SPLIT, todo=todo),
						icon='new_todo.png',
						valid=True)
	
	if todo_items == 0:
	
		for file_tuple in file_items:
			filename, file_obj = file_tuple
			file_icon = file_obj['icon']
			
			wf.add_item(title=filename, 
						subtitle='add new todo in todos/{}.md'.format(filename), 
						arg='{filename}{split}{todo}{split}add'.format(filename=filename, split=SPLIT, todo=arg),
						icon=file_icon,
						valid=True)

	wf.send_feedback()
	

if __name__ == '__main__':
	wf = Workflow3()
	logger = wf.logger
	sys.exit(wf.run(todo))