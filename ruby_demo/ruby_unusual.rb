#!/usr/lib/ruby
#异常unusual的处理
begin
   file=open("ruby_unusual.rb")
   if file
     puts "file open sucessfully"
   end
   rescue
      file=STDIN
end
print file,"==",STDIN,"\n"
