'''
这是一个用来处理时间列表的函数,其作用是将一个元素中的: - 符号 换成.,以规范数据使数据一致
'''
def sanitize(time_string):
    if '-' in time_string:
        splitize = '-'
        (mins, secs)=time_string.split(splitize)
    elif ':' in time_string:
        splitize = ':'
        (mins, secs)=time_string.split(splitize)
    else:
        return(time_string)
    return(mins+'.'+secs)    
