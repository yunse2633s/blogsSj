#!/usr/bin/ruby
#一个进程多个线程
def func1
	i=0
	while i<=2
		puts "func1 at:#{Time.now}"
		sleep(2)
		i=i+1
	end
end
def func2
	j=0
	while j<=2
		puts "func2 at:#{Time.now}"
		sleep(1)
		j=j+1
	end
end

puts "start at #{Time.now}"
t1=Thread.new{func1()}
t2=Thread.new{func2()}
# t1.join
# t2.join
# puts "End at #{Time.now}"

#----
# begin
# 	t=Thread.new do
# 		Thread.pass
# 		raise "unhandled exception"
# 	end
# 	t.join
# rescue
# 	p $! #=>"unhandled exception"

# end
#--使用锁定，实现线程同步
puts "synchronize thread"
@num=200
@mutex=Mutex.new
def buyTicket(num)
	@mutex.lock
		if @num>=num
			@num=@num-num
			puts "你成功购买到第#{@num}张票"
		else
			puts "你没成功"
		end
	@mutex.unlock
end
ticket1=Thread.new 10 do
	10.times do |value|
	ticketNum=20
	buyTicket(ticketNum)
	sleep 0.01
	end
end
ticket2=Thread.new 10 do
	10.times do |value|
	ticketNum=20
	buyTicket(ticketNum)
	sleep 0.01
	end
end

# sleep 1
# ticket1.join
# ticket2.join
10.times do |i|
 puts i
end