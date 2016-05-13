#!/usr/bin/ruby
#重命名文件test.txt为test4.txt
if File.file?("ruby_file.rb")
   File.rename("ruby_file.rb","ruby_file4.rb")
else
   puts "文件不存在，更名不成"
end

#删除
if File.file?("test.del.txt")
   File.delete("test.del.txt")
else
   puts "文件不存在,不用删除"
end



