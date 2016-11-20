import socket
import os

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print request
    req = request.split("\r\n")
    protocal = req[0].split(" ")
    try:
        filename = protocal[1]

    	if(protocal[0] == "POST"):
    		roomName = request[request.length-1].split("&")[0].split("=")[0]

    		if not os.path.exists('./data/'+roomName):
    			os.makedirs('./data/'+roomName))
    		room = open('./data/'+roomName+'/1', 'w+')

            pass
        else if (protocal[0] == "GET"):
            if(filename == "/"):
                rf = open('./serverfiles/index.html', 'r')
            else:
                rf = open('./serverfiles' + filename, 'r')

            filecontent = rf.read()
            http_response = """\
HTTP/1.1 200 OK

%s
"""
            pass
    except Exception as e:
        filecontent = ""
        http_response = """\
HTTP/1.1 404 Not Found

%s
"""

    client_connection.sendall(http_response  % (filecontent))
    client_connection.close()
