#=====================================堆排序=============================================================
#   有一个树。请打印出他的完全二叉树形式
#   分析：
# 非链式结构转换为链式结构最有效的方式就是投影（相当于从上向下平行的照射一束光，投影在一条线上）（降维）
# 类似于网页栅格系统
# |  |  |  |  |  |  |  30 |  |  |  |  |  |  |
# |  |  |  20 |  |  |  |  |  |  |  80 |  |  |
# |  40 |  |  |  50 |  |  |  10 |  |  |  60 |
# 70 |  90 |  |  |  |  |  |  |  |  |  |  |  |
# .  .  .  .  .  .  .  .  .  .  .  .  .  .  .


# 先确定最后一行的宽度，等于所有元素的投影(这个例子中为15也就是2的5次方减1，而5这个数字是二叉树的深度4+1（二叉树的性质5)),这样就能确定每行的空格数
# 第一行的前空格  7       第一行的两个数中间的宽度    0   #第一行只有一个元素定为0
# 第二行的前空格  3       第二行的两个数中间的宽度    7
# 第三行的前空格  1       第三行的两个数中间的宽度    3
# 第四行的前空格  0       第四行的两个数中间的宽度    1

# def show_tree(tree_list):
#   '''
# 自己写的不知道哪里出问题了，待改进
# 
# 核心思想计算每一行所要打印的数字，转换为字符串，然后中间插入指定宽度然后居中显示
#   


#     array = tree_list[:]
#     array.insert(0,0)   #将原有列表头部插入一个0，方便用下标引用
#     import math
#     depth = math.ceil(math.log2(len(array)))
#     sep = ' '*len(str(max(array)))  # 确定每个字符的宽度
#     width = len((sep * (depth-1)))-1
#     print('{:^{}}'.format(array[1],width))
#     for i in range(2,depth):
#         line = map(str,array[2 ** (i - 1):2 ** i]) # 使用map函数将要打印的数转化为字符串
#         print_line = sep.join(line)
#         print(print_line.center(width))
# #        print('{:^{}}'.format(print_line,width))
#     print(sep.join(map(str,array[2 ** (depth -1):])))

origin = [30,20,80,40,50,10,60,70,90]
def show_tree(tree_array):
    ''' 
    将一个序列以一个完全二叉树的形式打印

    第一行的前空格  7       第一行的两个数中间的宽度    0 
    第二行的前空格  3       第二行的两个数中间的宽度    7
    第三行的前空格  1       第三行的两个数中间的宽度    3
    第四行的前空格  0       第四行的两个数中间的宽度    1
    '''
    array = tree_array[:]
    array.insert(0,0)
    import math

    index = 1
    depth = math.ceil(math.log2(len(array)))
    sep = ' '*len(str(max(array)))      # 如果一个其中有一个数字太长的不判断他占的宽度就就有很奇怪的显示

    for i in range(depth):
        offset = 2 ** i
        print (sep * (2 ** (depth-i -1 )-1),end='')
        line = array[index:index + offset]
        for j,x in enumerate(line):
            print('{:>{}}'.format(x,len(sep)),end='')
            interval = 0 if i == 0 else 2 ** (depth- i) -1
            if j < len(line) -1:
                print(sep * interval,end='')
        index += offset
        print()
        
show_tree(origin)






