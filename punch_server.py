#!/usr/bin/env python
#
# Proof of Concept: TCP Hole Punching
# Two client connect to a server and get redirected to each other.
#
# This is the TCP server.
#
# Name : Nguyen Thanh Hiep
# 2014/06 IUH
#
 
import socket
import struct
import sys
import select
import string
import threading
def bytes2addr( bytes):
	"""Convert a hash to an address pair."""
	if len(bytes) != 6:
		raise (ValueError, "invalid bytes")
	host = socket.inet_ntoa( bytes[:4] )
	port, = struct.unpack( "H", bytes[-2:] )
	return host, port
def addr2bytes( addr):
    """Convert an address pair to a hash."""
    host, port = addr
    try:
        host = socket.gethostbyname( host )
    except (socket.gaierror, socket.error):
        raise (ValueError, "invalid host")
    try:
        port = int(port)
    except ValueError:
        raise (ValueError, "invalid port")
    bytes  = socket.inet_aton( host )
    bytes += struct.pack( "H", port )
    return bytes

class ClientThread(threading.Thread):

	    def __init__(self,client_address,connection,threads):
		threading.Thread.__init__(self)
		self.client_address = client_address
		self.connection = connection
		self.threads = threads
		
		print "[+] New thread started for ", client_address
	    def run(self):
		self.client = []
		print "connection from %s:%d" % self.client_address
		name = self.connection.recv(32)
	    	self.connection.send("ok" + name)
		print "received name"
		data = self.connection.recv(32)
		local = bytes2addr(data)
		self.connection.send("oklocal")
		print "received local"
		code = self.connection.recv(32)
		self.connection.send("okcode")
		print "received code"
		self.client.append(self.client_address)
		self.client.append(local)
		self.client.append(code)
		data = self.connection.recv(32)
		print "--- add pool ", ":" , self.client  
		print "--- request received for other Request Name: ", name
		
		no = len(self.threads)
		if no % 2 == 0:
		    print self.threads[no-2].client
		    a = self.threads[no-2].client
		    b = self.client
		    print "--- thiet lap ket noi giua cac Name: ", name
	    	    self.connection.send(addr2bytes(a[0]))
	    	    self.connection.send(addr2bytes(a[1]))
	    	    self.connection.send(a[2])
		    self.connection.send("RE")
	    	    self.threads[no-2].connection.send(addr2bytes(b[0]))
	    	    self.threads[no-2].connection.send(addr2bytes(b[1]))
	    	    self.threads[no-2].connection.send(b[2])
	    	    self.threads[no-2].connection.send("SE")
		    print "--- linked ---", name
		    print "--- ket noi hai may thanh cong ---"



def main():
    port = 8080
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        pass
 
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind( ("", port) )
    threads = []

    while True:
		s.listen(5)
		print "---TCP hole punching---"
		print "Listening on *:%d (tcp)" % port
		print "......................."
		connection, client_address = s.accept()
		newthread = ClientThread(client_address, connection, threads)
    		newthread.start()
    		threads.append(newthread)
		
		     
 
if __name__ == "__main__":
    main()
