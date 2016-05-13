#!/usr/bin/ruby
#创建哈希
months=Hash.new
_month = Hash.new("month")
_H = Hash["a"=>'我是数组',"b"=>200]
#
puts "输出months: #{months[72]}"
puts "输出哈希_month:#{_month[0]}"
puts "输出哈希_H:#{_H['a']}"
puts "输出哈希内置方法_H.keys:#{_H.keys}"
puts "#{_H.to_a}"
#迭代
_H.each do |i|
   puts "迭代#{i}"
end
#_h=Array.new
_h = _H.collect{|x|x}
puts "collect迭代器返回集合到所有元素#{_h}"
