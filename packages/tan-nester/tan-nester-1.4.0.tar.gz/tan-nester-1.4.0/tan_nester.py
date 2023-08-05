'''
这是"nester.py"模块，提供了一个名为 print_lol（）的函数，
函数的作用是打印列表
	
	'''
'''
version -1.3.0
添加了文件输出,如果不指定文件位置,则默认标准输出 fn=sys.stdout,将文件内容输出到屏幕

'''
import sys
def print_lol(the_list,indext=False,level=0,fn=sys.stdout):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indext,level,fn)
		else:
			if indext:
			   for tab_stop in range(level+1):
				   print("\t", end='',file=fn)
				   
			print(each_item,file=fn)
