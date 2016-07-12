"""
todo helpers
"""
# -*- coding: UTF-8 -*-
import os
import re
from random import randrange
from .const_value import TODO_HEADER, ACTIONS


def filter_complete_todos(todo):
	re_result = re.search(r'^{}~~(.*)~~\n$'.format(TODO_HEADER), todo)
	result = True if re_result else False
	return result


def filter_target_todo(argument):
	def filter_todo(todo):
		target_result = re.search(r'^{todo_header}.*{argument}.*\n$'.format(todo_header=TODO_HEADER, argument=argument), todo)
		complete_result = filter_complete_todos(todo)
		result = True if target_result and not complete_result else False
		return result
	return filter_todo


def get_todo_actions():
	all_actions = {}
	for action in ACTIONS:
		icon_path = 'icons/todo_{}.png'.format(action)
		action_icon = icon_path if os.path.isfile(icon_path) else get_default_icon()
		all_actions[action] = action_icon
	return all_actions


def get_default_icon():
	default_icons = os.listdir('icons/default')
	return 'icons/default/{}'.format(default_icons[randrange(0, len(default_icons))])
