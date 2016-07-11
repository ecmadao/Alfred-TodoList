# -*- coding: utf-8 -*-
import sys
import re
from workflow import Workflow3
from todos_files import todo_files
from const_value import SPLIT

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

	for item in file_items:
		filename, file_obj = item
		for todo in file_obj['todos']:
			if re.search(r'\[@(\d*.*)\]$', todo):
				todo, todo_time = re.findall(r'(.+)\[@(.*)\]$', todo)[0]
			else:
				todo_time = 'has no record yet.'
			wf.add_item(title=todo,
						subtitle='{filename} create at: {todo_time}'.format(filename=filename, todo_time=todo_time),
						arg='{filename}{split}{todo}'.format(filename=filename, split=SPLIT, todo=todo),
						icon='new_todo.png',
						valid=True)

	wf.send_feedback()


if __name__ == '__main__':
	wf = Workflow3(update_settings={
		'github_slug': 'ecmadao/Alfred-TodoList',
		'frequency': 4
	})
	logger = wf.logger
	sys.exit(wf.run(todo_filter))
	if wf.update_available:
		wf.start_update()
