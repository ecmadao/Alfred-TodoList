# -*- coding: utf-8 -*-
import sys
import re
from workflow import Workflow3
from todos_files import todo_files
from const_value import SPLIT

reload(sys)
sys.setdefaultencoding('utf-8')


def todo_new(wf):
	if len(wf.args):
		try:
			arg = re.findall(r'new: (.*)', ''.join(wf.args))[0]
		except IndexError:
			if arg != None then arg = arg else arg = ''
	else:
		arg = ''

	file_object = todo_files(arg)
	file_items = file_object.files.items()

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
	wf = Workflow3(update_settings={
		'github_slug': 'ecmadao/Alfred-TodoList',
		'frequency': 4
	})
	logger = wf.logger
	sys.exit(wf.run(todo_new))
	if wf.update_available:
		wf.start_update()
