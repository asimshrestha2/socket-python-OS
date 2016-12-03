import socket
import os
import io
from requestapp import Requestapp

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(4)
print 'Serving HTTP on port %s ...' % PORT
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print request
    req = request.split("\r\n")
    protocal = req[0].split(" ")
    try:
        filename = protocal[1]
        print filename

        if (protocal[0] == "POST"):
            dataArray = req[len(req)-1].split("&")

            #print dataArray
            data = {}
            for dataEntry in dataArray:
                #print dataEntry
                naval = dataEntry.split('=')
                data[naval[0]] = naval[1]
            print data

            if (filename == "/update"):
                newfile = False
                if not os.path.exists('./data/'+data['room']):
                    newfile = True
                    os.makedirs('./data/'+data['room'])

                roomdata = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8')

                if newfile or roomdata.read() == "":
                    roomdata.write(u'0,0\n')

                roomdata.close();
                filecontent = ""
                with open('./data/'+data['room']+'/1', 'r') as f:
                    filecontent = f.read()

                print filecontent
                http_response = Requestapp(filename, filecontent).getResponse()


        elif (protocal[0] == "GET"):
            if(filename == "/"):
                rf = open('./serverfiles/index.html', 'r')
                filename = "/index.html"
            else:
                rf = open('./serverfiles' + filename, 'r')

            filecontent = rf.read()
            http_response = Requestapp(filename, filecontent).getResponse()
    except Exception as e:
        print e
        http_response = Requestapp("", "", 404).getResponse()

    client_connection.sendall(http_response)
    client_connection.close()
