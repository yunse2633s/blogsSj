#!/usr/bin/ruby
# -*- coding:UTF-8 -*-

def test
   puts "在test方法内";
   yield
   puts "你又回到类test方法内";
   yield
end
test {puts "你在快内"}


def test2
   yield 5
   puts "在test方法内"
   yield 10
end
test2 {|i|puts "你在快#{i}内"}
