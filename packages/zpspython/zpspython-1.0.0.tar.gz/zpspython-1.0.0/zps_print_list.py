def print_list(the_list):
	for each in the_list:
		if isinstance(each,list):
			print_list(each)
		else:
			print(each)