#!/usr/lib/ruby
begin
   # ..抛出异常
   raise 'A test exception.'
   rescue Exception =>e
   #..处理错误
     puts e.message
     puts e.backtrace.inspect
   else
     puts "Congratulations--no errors"
   ensure
   #..总会执行
     puts "Ensuring execution"
end
