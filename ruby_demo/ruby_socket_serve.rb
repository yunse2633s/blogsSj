#!/usr/lib/ruby
require 'socket'
server=TCPSocket.open('127.0.0.1',10089)
loop{
	client=server.accept
	client.puts(Time.now.ctime)
	client.puts "Closing the connection.Bye"
	client.close
}