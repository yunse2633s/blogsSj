#!/usr/lib/ruby
# 访问控制，继承，重载
class Box
    #构造方法
    def initialize(w,h)
       @width,@height=w,h
    end
    #实例方法默认是public的
    def getArea
       getWidth()*getHeight
    end
    #定义private的访问器方法
    def getWidth
       @width
    end
    def getHeight
       @height
    end
    #设置为私有方法
    private :getWidth,:getHeight
    #用于输出面积到实例方法
    def printArea
      @area=getWidth()*getHeigth
      puts "盒子到面积:#{@area}"
    end
    #设置保护的方法
    protected:printArea

end

#创建对象
 box=Box.new(10,20)
#调用实例方法
 a=box.getArea()
puts "面积#{a}"
#box.printArea()
puts "-----"
#尝试调用受保护到方法
begin
   box.printArea()
   raise 'box.printArea()执行错误'
   rescue Exception=>e
      puts e.message
      puts e.backtrace.inspect
   ensure
   #Box.printArea()
   #puts "box.printArea()执行"
   puts "出错依然继续"   
end
