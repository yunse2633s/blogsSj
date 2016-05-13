#!/usr/bin/ruby

#文件到查询
if File::exists?("ruby_demo1.rb")
   puts "ruby_demo文件存在"
end
if File.file?("ruby_demo1.rb")
   puts "ruby_demo是一个文件而非文件夹"
end
if File::directory?("/home/sujian")
   puts "/home/sujian是一个文件夹"
end
if File.readable?("ruby_demo1.rb")
   puts "ruby_demo.rb是可读"
end
if File.writable?("ruby_demo1.rb")
   puts "ruby_demo文件可写"
end
if !File.executable?("ruby_demo1.rb")
   puts "ruby_demo文件不可执行"
end





