#!/usr/bin/ruby
#运算符重载
class Box
    def initialize(w,h)
       @width,@heigth=w,h
    end
    def +(other)
       Box.new(@width+other.width,@height+oter.height)
    end
end
box = Box.new(10,20)
puts box.+(2)
