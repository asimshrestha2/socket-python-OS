import socket

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    req = request.split("\r\n")
    protocal = req[0].split(" ")
    filename = protocal[1]
    if(filename == "/"):
        rf = open('./serverfiles/index.html', 'r')
    else:
        rf = open('./serverfiles' + filename, 'r')
    
    filecontent = rf.read()
    http_response = """\
HTTP/1.1 200 OK

%s
"""
    client_connection.sendall(http_response  % (filecontent))
    client_connection.close()
