import socket
import os, sys
import io
from requestapp import Requestapp
from room import Room #room class for each room will be pointers to 2 sockets

HOST, PORT = '', 8888
rooms = {}

#we need a dictionary to make sure if the players aren't joining the room
#at the same time, they can be put in the correct array
#dictionary array manage game: Key: Room # Value:2D array with both sockets
#class room is the 2d array

#---FUNCTIONS---
#one thread will be accepting stuff
def acceptConnections(listen_socket):
    client_connection, client_address = listen_socket.accept()
    print "Got connection from %s." % client_address[0]
    return client_connection, client_address
    
#This function will contain game logic -- we need two socket desriptors one for
#each party in the game.  Use this function in a thread sil vous plait
#playerSockets - 2 sockets representing two players.  p1 = 0, p2 = 1                     
def manageGame(playerSockets):
    submitRequests = 0 #how many players made a choice so far
    return

def getWinner(player1data, player2data, roomnum):
    print player1data == 1
    print player2data == 1

    if((player1data == 1 and player2data == 2) or
       (player1data == 2 and player2data == 3) or
       (player1data == 3 and player2data == 1)):
        return 2
    elif((player2data  == 1 and player1data == 2) or
       (player2data == 2 and player1data == 3) or
       (player2data == 3 and player1data == 1)):
        return 1
    else:
        return 0
    
#--MAIN PROGRAM--
#get socket file descriptor for this computer
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#if the port isn't free, lets clear it
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#listen on this port with this socket... aka call me maybe
listen_socket.bind((HOST, PORT))

#number of connection allowed to queue up
listen_socket.listen(5)

print 'Serving HTTP on port %s ...' % PORT
while True:
    client_connection, client_address = acceptConnections(listen_socket)
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
            data = {} #dictionary of key value pairs
            
            for dataEntry in dataArray:
                #set up a dictionary using the key value pairs in the content
                naval = dataEntry.split('=')
                data[naval[0]] = naval[1]
            print data

            roomNum = data["room"]
            #if our request-uri is update
            if (filename == "/start"):
                #since it's our first time lets add this socket to our rooms
                #add player to our Room class

                if not roomNum in rooms:
                    rooms[roomNum] = Room()

                #add our connection to that room
                rooms[roomNum].sockets.append(listen_socket)

                #send an http response so it can tell what player it is
                print "HTTP REPONSE:"
                #return to it player number
                filecontent = str(len(rooms[roomNum].sockets))
                http_response = Requestapp(filename, filecontent).getResponse()
                client_connection.sendall(http_response)
                client_connection.close()

            elif (filename == "/update"):
                if(data["player"] == 1):
                    rooms[roomNum].values[0] = data["choice"]
                elif(data["player"] == 2):
                    rooms[roomNum].values[1] = data["choice"]
                else:
                    print "Error"
                    
                if(len(rooms[roomNum].values) > 2): #if we have both responses
                    winner = getWinner(roomNum, rooms[roomNum].values[0],rooms[roomNum].values[1])
                    filecontent = str(winner)
                    ttp_response = Requestapp(filename, filecontent).getResponse()
                    client_connection.sendall(http_response)
                    client_connection.close()

            else:
                for s in rooms[roomNum].sockets:
                    s.close()                
                del rooms[roomNum].sockets[:]          
        elif (protocal[0] == "GET"):
            if(filename == "/"):
                rf = open('./serverfiles/index.html', 'r')
                filename = "/index.html"
            else:
                rf = open('./serverfiles' + filename, 'r')

            filecontent = rf.read()
            rf.close()
            http_response = Requestapp(filename, filecontent).getResponse()
    except Exception as e:
        lineNum = sys.exc_info()[2].tb_lineno
        print lineNum
        print e
        http_response = Requestapp("", "", 404).getResponse()
        client_connection.sendall(http_response)
        client_connection.close()
                    
