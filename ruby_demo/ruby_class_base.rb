#!/usr/lib/ruby
class Box
  #输出类信息
  puts "class of self=#{self.class}"
  puts "类名=#{self.name}"

end

box=Box.new
puts box
#
class Box1
  puts "类名#{self.name}"
  #构造函数
  def initialize(w,h)
    @width,@height = w,h
  end
  #常量
  BOX_COMPANY="sujian"
  #访问器方法
  def printWidth
    @width
  end
  def printHeight
    @height
  end
  #设置器方法
  def setWidth=(value)
     @width=value
  end
  def setHeight=(value)
     @height=value
  end
  #
end
box1=Box1.new(2,3)
#使用访问器方法
puts "box1类中到方法调用#{box1.printWidth()}"
#使用设置器方法
box1.setWidth=50
puts "在使用设置器方法后，使用访问器方法获取新值#{box1.printWidth()}"
#类方法 和 类变量
class Box2
  puts "类名#{self.name}"
  #初始化类变量
  @@count = 0
  def initialize(w,h)
    #给实例变量赋值
    @width,@height=w,h
    @@count +=1
  end
  def self.printCount()
    puts "box2 counts is :#{@@count}"
  end
  #自动调用到方法
  def to_s
    "(w:#{@width},h:#{@height})"
  end
end
#实例化
box2=Box2.new(10,20)
box21=Box2.new(30,100)
#allocate 创建未初始化到对象(即不调用对象构造器initialize
box22=Box2.allocate;
puts "调用类方法来输出实例化到次数#{Box2.printCount()}"
puts "使用to_s,类中自主执行到方法: #{box2.to_s()}"
puts "输出常量值:#{Box1::BOX_COMPANY}"
puts "allocate实例化到对象没有调用对象构造器"
puts "请输出#{box22.pintCount()}"
