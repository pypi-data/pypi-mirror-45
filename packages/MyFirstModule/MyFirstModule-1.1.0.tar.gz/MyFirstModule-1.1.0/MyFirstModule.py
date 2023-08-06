
"""这是一个模块，里面有一个处理列表的函数"""
def print_lol(the_list,level):
    """这个函数的功能是打印一个列表中的列表项，
如果列表内有嵌套列表，则将嵌套列表中的数据项也打印在屏幕上"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)
