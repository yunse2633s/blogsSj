#!/usr/bin/ruby -w
#继承
#定义类
class Box
    #构造器方法
    def initialize(w,h)
      @width,@height=w,h
    end
    #实例方法
    def getArea
      @width * @height
    end

end
#定义子类
class BigBox < Box
  #添加一个新到实例方法
  def printArea
     @area=@width*@height
     puts "Big box area is :#@area"
  end
end
#创建对象
box=BigBox.new(10,20)
#输出面积
box.printArea()
puts "调用上级到方法:#{box.getArea()}"
##方法重载
class RepeatBox<Box
  #改变已有到getArea方法
  def getArea
     @area=@width*@height*2
     puts "2倍盒子的面积:#@area"
  end
end
#创建Object
repBox=RepeatBox.new(10,20)
repBox.getArea()
#类到冷冻
repBox.freeze
if(repBox.frozen?)
  puts "repBox is frozen object"
else
  puts "repBox is normal object"
end
puts "--------"
repBox.getArea()

