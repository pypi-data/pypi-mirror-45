"""nester-lupiani.py contains the function print_lol() which will return your list even it if contains nested lists"""

def print_lol(the_list):
	"""The function takes each item in the list, check to see if that item is a list, if it is, it repeats the function, if not, it prints the list item"""
	
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item)
		else:
			print(each_item)
