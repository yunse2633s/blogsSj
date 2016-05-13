#!/usr/bin/ruby
#$,="+ "
range1=(1..10).to_a
puts "#{range1}"

#
digits = 0..9
puts digits
puts digits.include?(5)
puts "最小为#{digits.min},最大为#{digits.max}"

#循环
digits.each do |digit|
  puts "循环进行中 #{digit}"
end
#
ret=digits.reject{|i|i<5}
puts "不符合条件的#{ret}"
#Range作为条件范围
score=70;
result=case score
when 0..40
     "糟糕到选择"
when 41..60
    "危险到决定"
when 61..70
    "沉迷安逸"
when 71..100
    "绝地重生"
else
    "错误人生"
end
puts result;

#作为间隔到范围
if(('a'..'j')==='c')
   puts "c在('a'..'j')之间"
end
if((1..10)===5)
   puts "5在(1..10)之间"
end


