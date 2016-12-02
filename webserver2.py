import socket
import os
import io
from requestapp import Requestapp
from room import Room #room class for each room will be pointers to 2 sockets

HOST, PORT = '', 8888

#we need a dictionary to make sure if the players aren't joining the room
#at the same time, they can be put in the correct array
#dictionary array manage game: Key: Room # Value:2D array with both sockets
#class room is the 2d array

sockets = []
rooms = []

#---FUNCTIONS---
#one thread will be accepting stuff
def acceptConnections(listen_socket):
    while True:
        client_connection, client_address = listen_socket.accept()
        print "Got connection from %s." % socket.inet_ntop(AF_INET, client_address)
        sockets.append(client_connection)
    
#This function will contain game logic -- we need two socket desriptors one for
#each party in the game.  Use this function in a thread sil vous plait
#playerSockets - 2 sockets representing two players.  p1 = 0, p2 = 1                     
def manageGame(playerSockets):
    submitRequests = 0 #how many players made a choice so far

#--MAIN PROGRAM--
#get socket file descriptor for this computer
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#if the port isn't free, lets clear it
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#listen on this port with this socket... aka call me maybe
listen_socket.bind((HOST, PORT))

#number of connection allowed to queue up
listen_socket.listen(10)

print 'Serving HTTP on port %s ...' % PORT
while True:
    
    #get me client file descriptor returns pair conn address 
    #client_connection, client_address = listen_socket.accept()
    acceptConnections(listen_socket);

    #get that http request information into a buffer
    request = client_connection.recv(1024)
    
    print request
    req = request.split("\r\n")

    #first chunk of data from first line is the verb 
    protocal = req[0].split(" ")
    try:
        filename = protocal[1]
        print filename

        #recieving information
        if (protocal[0] == "POST"):
            #the last line is typically the content which we are analyzing here
            dataArray = req[len(req)-1].split("&")
            
            data = {}
            
            for dataEntry in dataArray:
                #set up a dictionary using the key value pairs in the content
                naval = dataEntry.split('=')
                data[naval[0]] = naval[1]
            print data

            #if our request-uri is update
            if (filename == "/update"):
                newfile = False
                #and the update folder is not there make a new one
                if not os.path.exists('./data/'+data['room']):
                    newfile = True
                    os.makedirs('./data/'+data['room'])

                    
                #else open that room file
                roomdata = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8')

                #if newfile, this is the default first entry
                #if newfile or roomdata.read() == "":
                #    roomdata.write(u'0,0\n')

                
                roomdata.close();
                filecontent = ""
                with open('./data/'+data['room']+'/1', 'r') as f:
                    filecontent = f.read()

                print filecontent
                http_response = Requestapp(filename, filecontent).getResponse()
            #if our request-uri is root, we're getting information from the game
            else:
                submitRequests = 0
               # while(submitRequests !
                

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
                    
