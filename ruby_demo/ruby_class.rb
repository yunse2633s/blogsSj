#!/usr/bin/ruby
class Sample
   def hello
	puts "hello Ruby!"
   end
end

object = Sample.new;
object.hello;
#参数, 类中变量：局部，实例，类，全局
class Customer
   @@no_of_customers=0;
   def initialize(id,name,addr)
	@cust_id=id;
	@cust_name=name;
	@cust_addr=addr;
	puts @cust_id+'--'+@cust_addr
   end
end

cust1 = Customer.new('1','John','how are you');
puts "源文件到名称" +  __FILE__

#定义方法
def add(x,y)
   puts "#{x+y}";
   return x+y+1; 
end
puts "调用方法add()"
@c = add(1,3);
puts @c
