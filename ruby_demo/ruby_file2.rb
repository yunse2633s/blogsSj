#!/usr/bin/ruby
# -*- cading:UTF-8 -*-
#aFile = File.new("ruby_txt2.txt","w+")
#if aFile
#    content= aFile.sysread(6)
#    puts content
#    aFile.syswrite("ABCD")
#else
#    puts "无法打开"
#end

#####
#aFile = File.new("ruby_txt2.txt","r+")
#if aFile
#    aFile.syswrite("ABCDEF")
#    aFile.rewind
#    aFile.each_byte{|ch|putc ch;putc ?.}
#else
#    puts "no file"
#end

####
arr = IO.readlines("ruby_txt.txt")
puts arr[3]
puts "#{arr}"

