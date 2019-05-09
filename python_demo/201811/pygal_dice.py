import random

class Die:
    """
    一个骰子类
    """
    def __init__(self, num_sides=6):
        self.num_sides = num_sides
        
    def roll(self):
        return random.randint(1, self.num_sides)


import pygal
die = Die()
result_list = []
# 掷1000次
for roll_num in range(1000):
    result = die.roll()
    result_list.append(result)
    
frequencies = []
# 范围1~6，统计每个数字出现的次数
for value in range(1, die.num_sides + 1):
    frequency = result_list.count(value)
    frequencies.append(frequency)
    
# 条形图
hist = pygal.Bar()
hist.title = 'Results of rolling one D6 1000 times'
# x轴坐标
hist.x_labels = [1, 2, 3, 4, 5, 6]
# x、y轴的描述
hist.x_title = 'Result'
hist.y_title = 'Frequency of Result'
# 添加数据， 第一个参数是数据的标题
hist.add('D6', frequencies)
# 保存到本地，格式必须是svg
hist.render_to_file('die_visual.svg')