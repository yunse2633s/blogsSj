#!/usr/bin/ruby -w
# -*- coding:UTF-8 -*-
puts 2**(1/4);
puts 'That\'s right';
puts 'escape using "\\"';
puts '单引号转义 \'is';
puts '单引号下数 value: #{2+2}';
puts "双引号下 value: #{1+2}";
name="Ruby字符串链接符+";
puts "#{name + ",双引号套接双引号"}"
puts "循环对象元素";
hsh=colors={"red"=>0xf00,"green"=>0x0f0,"blue"=>0x00f};
hsh.each do | key, value |
	print key," is ",value,"\n"
end
