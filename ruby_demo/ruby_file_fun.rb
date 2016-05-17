#!/usr/bin/ruby
# -*-类方法Obj::funName 实例方法Obj.funName-*-
path="/home/ruby"
isDir=File::directory?(path)
puts "ruby是文件夹吗#{isDir}"
#时间
fileName="/home/ruby/ruby_arith.rb"
isCtime=File::ctime("/home/ruby/ruby_arith.rb")
#isAtime=File::ctime("ruby_arith.rb")
puts "文件创建时间#{isCtime}"
#大小
isSize=File.size(fileName)
puts "fileName文件大小#{isSize}"
#文件类型
isFtype=File::ftype(fileName)
puts "fileName文件类型#{isFtype}"
#获取文件目录
puts Dir.pwd
#创建目录
if !File::directory?("mytmpdir")
  puts "mytmpdir文件夹不存在"
  Dir.mkdir("mytmpdir")
  puts "mytmpdir文件夹创建成功"
end
#for i in 0..5
 # puts "#{i}"
#end
#$定义全局变量
$i=0
$num=5
while $i<$num do
   puts "#{$i},mytmpdir是否为目录:#{File::directory?("mytmpdir")}";
   $i+=1;
end
#删除目录
if File::directory?("mytmpdir")
   puts "准备删除mytmpdir文件夹"
   Dir.delete("mytmpdir")
   puts "mytmpdir文件已经删除"
end

