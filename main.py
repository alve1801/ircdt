#!/usr/bin/env python
import socket
import threading
import time # for delays

login='''HTTP/1.1 200 OK\r\n\r\n<!DOCTYPE html>
<div style="width:50%;margin: 0 auto;text-align:center;">
please enter login:
<form method="post" id="login">
	<input type="text" id="uname" name="uname" minlength=3 maxlength=8 size=10 placeholder="username"><br>
	<input type="submit" value="enter">
</form><div>
'''

page='''HTTP/1.1 200 OK\r\n\r\n<!DOCTYPE html>
<div style="width:50%;margin: 0 auto;">
{0}
<div style="width:20%;float:left;">{1}</div>
<div style="width:80%;float:left;">
<form method="post" id="msg">
	<input type="text" size=50 name="msg"/>
	<input type="hidden" name="uname" value="{1}"/>
	<input type="submit" value="send">
</form>
<form method="post"><input type="submit" value="load new messages"><input type="hidden" name="uname" value="{1}"/></form>
</div></div>'''

msgformat='''<hr>
<div style="width:20%;float:left;">{}</div>
<div style="width:80%;float:left;overflow-wrap:break-word;">{}</div>
<br>'''

history=[]

def handle_echo(client_connection, client_address):
	global history # because python is a bit stupid
	client_connection.settimeout(30)
	try:
		print("\n\nnew connection from {}".format(client_address))
		alldata=b''
		while 1:
			data = client_connection.recv(1024)
			alldata+=data
			# XXX update the following when we fix it in main
			if len(data)<1024:break
			time.sleep(.001)

		alldata=alldata.decode()

		uname=alldata.find('uname=')
		if(uname==-1):response=login
		else:
			endname=alldata.find('\n',uname)
			if endname==-1:uname=alldata[uname+6:]
			else:uname=alldata[uname+6:endname]
			msg=alldata.find('msg=')
			if(msg!=-1):
				msg=alldata[msg+4:alldata.find('&',msg+4)]
				history+=[(uname,msg)]
			response=page.format(
				''.join([msgformat.format(i[0],i[1]) for i in history[-20:]])
				,uname)

		client_connection.send(bytes(response,'utf-8'))

	except socket.timeout:print('timeout')
	client_connection.shutdown(1)
	client_connection.close()
	print('done with {}'.format(client_address))

def listen(host, port):
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	conn.bind((host, port)),conn.listen(5)
	while 1:
		current_conn, client_address = conn.accept()
		print('{} connected'.format(client_address))
		handler_thread = threading.Thread(
			target = handle_echo,
			args = (current_conn,client_address)
		)
		handler_thread.daemon = 1
		handler_thread.start()

try:listen('0.0.0.0',8000)
except KeyboardInterrupt:pass
#logfile.close()

'''
reusing the file uploader, but this gonna be a web-based irc(like) server - with no js whatsoever!
all the magic happens by preformatting cookies into the pages, and checking those
name's "i really cant do this"

index page is login. form allows user to set a username, which is stored in the server.
loop
	server gets request. last part of request tells us username and (optionally) message to post
		update chat history if there was a message
	generate webpage w/ chat history, preformat username into form field so it gets sent w/ next request
end loop

page has a "post" textfield+button and a separate "reload" button to update history w/out sending a message. button triggers a page reload - username should still be in header

first figure out how to accomplish this in raw html ("manually"), then figure out the database & formatting stuff

could reduce it even further by making every request w/out a username default to login

form.method=post and what was the other one? where we just appended it to url w/ a question mark?
get (duh)
post might be more useful, since parsing it server-side should be easier (also, prolly a good idea not to transmit the messages via url)

apparently theres also a hidden type? this seems useful

---

textarea is a bit messy, tho it might work w/ the new formatting
encoding fucks up

timestamps?

'''
