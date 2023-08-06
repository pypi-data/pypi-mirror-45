def print_lol (list_name):
	for each in list_name:
		if (isinstance(each,list)):
			print_lol(each)
		else:
			print(each)