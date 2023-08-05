'''
这是"nester.py"模块，提供了一个名为 print_lol（）的函数，
函数的作用是打印列表
	test 03
	'''

def print_lol(the_list,indext=False,level=0):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indext,level)
		else:
			if indext:

			   for tab_stop in range(level):
				   print("\t", end='')
			print(each_item)
