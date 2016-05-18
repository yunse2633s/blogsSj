#!/usr/lib/ruby
require 'socket'
hostname='localhost'
port=20000
s=TCPSocket.open('127.0.0.1',2000)
while line = s.gets
	puts line.chop
end
s.close