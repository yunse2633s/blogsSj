#!/usr/bin/ruby

#输出File对象
num=0
xys={"a"=>'因为',"b"=>'所以'}
#xys.each do |key,value|
 # print key," is ",value,"\n"
#end
#打印对象中到内容;或读取对象到属性
for i in xys  
  print  i,"\n"
end
#输出对象到属性
#puts xys.a
s = "hello"
puts "字符串提取:#{s[2..3]}"
puts "字符串提取:#{s[-2..-1]}"
puts "字符串提取:#{s[0..0]}"
puts "数据类型-哈希:#{xys['a']}"

