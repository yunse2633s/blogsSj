#!/usr/lib/ruby
# -*- coding:UTF-8 -*-
_string = "abcdef"
puts _string
puts _string*3
puts _string + '你'
puts _string <=> 'ni'
puts _string.capitalize
puts _string.chop
puts _string.crypt('cc')
puts _string.delete('cde')
puts _string.hash

#日期
time1 = Time.new
puts "当前时间:"+time1.inspect
time2 = Time.now
puts "当前时间:"+time2.inspect
puts "日期年分#{time1.year}"

#范围
range1 = (1..10).to_a
puts "#{range1}"
