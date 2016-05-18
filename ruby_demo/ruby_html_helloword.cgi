#!/usr/bin/ruby
puts "HTTP/1.0 200 OK"
puts "Content-type:text/html\n\n"
puts "<html><body>hello world</body></html>"

# require "cgi"
# cgi=CGI.new("html4")
# cgi.out{
# 	cgi.html{
# 		cgi.head{"\n"+cgi.titl{"This is a Test"}}+
# 		cgi.body{"\n"+
# 			cgi.form{"\n"+
# 				cgi.hr+
# 				cgi.h1{"A Form:"}+"\n"+
# 				cgi.br +
# 				cgi.submit
# 			}
# 		}
# 	}
# }
# puts cgi.header
# puts "<html><body>hello world</body></html>"