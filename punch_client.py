#!/usr/bin/env python
#
# Proof of Concept: TCP Hole Punching
# Two client connect to a server and get redirected to each other.
#
# This is the client.
#
# Nguyen Thanh Hiep
# 2014/06 IUH
#
 
import sys
import socket
from select import select
import struct
import os
import time
import random, string, md5
import threading
from threading import Thread

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
def bytes2addr( bytes):
	"""Convert a hash to an address pair."""
	if len(bytes) != 6:
		raise (ValueError, "invalid bytes")
	host = socket.inet_ntoa( bytes[:4] )
	port, = struct.unpack( "H", bytes[-2:] )
	return host, port
def random_char(n):
	return ''.join(random.choice(string.ascii_letters) for x in range(n))
def creat_md5():
	m = md5.new(random_char(8))
	return m.hexdigest()
	
def main():
	try:
		server, port = sys.argv[1], int(sys.argv[2])
		name = sys.argv[3].strip()
	except (IndexError, ValueError):
		print ("usage: %s <host> <port> <pool>" % sys.argv[0])
		sys.exit(65)
	code = creat_md5()
	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.connect((server, port))
	s.send(name)
	while not s.recv(len(name) + 3) == "ok"+ name:
  		s.send(name)
	local = s.getsockname()
	s.send(addr2bytes(local))
	while not s.recv(32) == "oklocal":
  		s.send(addr2bytes(s.getsockname()))
	s.send(code)
	while not s.recv(32) == "okcode":
  		s.send(code)
	s.send("ok")
	print ("--- Request sent, waiting for parkner in Name '%s'..." % name)	
	
	target= s.recv(6)
	tlocal = s.recv(6)
	tcode = s.recv(32)
	stt = s.recv(32)
	tg = bytes2addr(target)
	tl = bytes2addr(tlocal)
	h, p = s.getsockname()
	print tg, tl, tcode, stt, h, p
	tloh, tlop = tl
	targeth, targetp = tg
	s.close()

	sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sc.bind( ("", p) )
	print "create connect to" , targeth, targetp
	sc.connect((targeth, targetp))
	print "peer connected to " , targeth, targetp
	while True:
		rfds,_,_ = select( [0, sc], [], [] )
			if 0 in rfds:
				data = sys.stdin.readline()
				if not data:
					break
				sc.send(data))
			elif sc in rfds:
				data = sc.recv(1024)
				sys.stdout.write( data )
	sc.close()

 
if __name__ == "__main__":
    main()
