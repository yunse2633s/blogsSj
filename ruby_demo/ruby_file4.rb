#!/usr/bin/ruby
aFile=File.new("ruby_txt.txt","r")
puts "流文件 #{aFile}"
aFile.each do |i|
   puts i
end
#文件已经到结尾，为何aFile 和 bFile不一样到变量
bFile=File.new("ruby_txt.txt","r+")
if bFile
    content=aFile.syswrite("sysread 和syswrite")
    puts content
else
    puts "不能打开"
end
