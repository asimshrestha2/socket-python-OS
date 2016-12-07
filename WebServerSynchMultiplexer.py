import socket
import select #select - Synchronous I/O Multiplexing
import os
import io
import time
from requestapp import Requestapp

#---FUNCTIONS---
def acceptConnections(listen_socket):
    client_connection, client_address = listen_socket.accept()
    print "Got connection from %s." % client_address[0]
    return client_connection, client_address

#Accesses both player data files, and returns either 1 or 2 for which player won
def getWinner(roomnum):
    roomdata1 = io.open('./data/'+ roomnum +'/1', 'r', encoding='utf8')
    roomdata2 = io.open('./data/'+ roomnum +'/2', 'r', encoding='utf8')
    player1data = roomdata1.read().encode('utf-8')
    player2data = roomdata2.read().encode('utf-8')
    roomdata1.close()
    roomdata2.close()

    player1data = int(player1data.split("\n")[0].split(",")[1])
    player2data = int(player2data.split("\n")[0].split(",")[1])

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

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

inputW = [listen_socket] #list of read sd's.  Needs one param so select doens't fail
writeW = [] #list of write sd's

listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(4)
print 'Serving HTTP on port %s ...' % PORT
while True:
    inputR, outputR, exceptR = select.select(inputW,writeW,[]) #without timeout, blocks until one fd is ready
    
    for s in inputR:#loop through read fds
        if s == listen_socket: #this is where we accept new connections
            client_connection, client_address = acceptConnections(listen_socket)      
            inputW.append(client_connection)
        else: #we got a connection we have to read from
            request = client_connection.recv(1024)
            print request
            req = request.split("\r\n")
            protocal = req[0].split(" ")
            try:
                filename = protocal[1]
                print filename

                if (protocal[0] == "POST"):
                    dataArray = req[len(req)-1].split("&") #data header will always be at end of request

                    #split and print dataArray (the data from reuqest)
                    data = {}
                    for dataEntry in dataArray:
                        #print dataEntry
                        #room = an arbritrary number
                        #player = 1 or 2
                        #item = 1, 2, or 3 (for rock/paper/scissors)
                        naval = dataEntry.split('=')
                        data[naval[0]] = naval[1]

                    print data

                    if(filename == "/newroom"):
                        if not os.path.exists('./data/'+data['room']):
                            #make directories
                            os.makedirs('./data/'+data['room'])

                            #make player 1 data file
                            roomdata = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8')
                            roomdata.write(u'1,0\n')
                            roomdata.close()

                            #make player 2 data file
                            roomdata = io.open('./data/'+data['room']+'/2', 'w+', encoding='utf8')
                            roomdata.write(u'0,0\n')
                            roomdata.close()

                            #respond that theyre player 1
                            http_response = Requestapp(filename, "player=1").getResponse()

                        else: #if room does exist
                            roomdata1 = io.open('./data/'+data['room']+'/1', 'r', encoding='utf8')
                            roomdata2 = io.open('./data/'+data['room']+'/2', 'r', encoding='utf8')
                            player1data = roomdata1.read().encode('utf-8')
                            player2data = roomdata2.read().encode('utf-8')
                            roomdata1.close()
                            roomdata2.close()

                            player1data = player1data.split("\n")[0].split(",")
                            player2data = player2data.split("\n")[0].split(",")

                            print player1data[0] == '1'
                            print player2data[0] == '1'

                            #if only player 1 is in the room
                            if(player1data[0] == '1' and player2data[0] == '0'):
                                roomdata = io.open('./data/'+data['room']+'/2', 'w+', encoding='utf8')
                                roomdata.write(u'1,0\n')
                                roomdata.close()
                                #at this point, both players are now in the room

                                http_response = Requestapp(filename, "player=2").getResponse()

                            #if only player 2 is in the room
                            elif(player1data[0] == '0' and player2data[0] == '1'):
                                roomdata = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8')
                                roomdata.write(u'1,0\n')
                                roomdata.close()
                                #at this point, both players are now in the room

                                http_response = Requestapp(filename, "player=1").getResponse()

                            #room is full
                            elif(player2data[0] == '1' and player1data[0] == '1'):
                                http_response = Requestapp(filename, "player=-1").getResponse()

                            else:
                                http_response = Requestapp(filename, "player=-1").getResponse()

                    elif(filename == "/update"):
                        #If player 1, check player 2 data file to check if theyre there
                        roomdata1 = io.open('./data/'+data['room']+'/1', 'r', encoding='utf8')
                        roomdata2 = io.open('./data/'+data['room']+'/2', 'r', encoding='utf8')
                        player1data = roomdata1.read().split("\n")[0].split(",")
                        player2data = roomdata2.read().split("\n")[0].split(",")
                        roomdata1.close()
                        roomdata2.close()

                        if(data['player'] == '1' ):
                            if(player2data[0] != '1'):
                                http_response = Requestapp(filename, "winner=0").getResponse()

                        #If player 2, check player 1 data file to check if theyre there
                        elif(data['player'] == '2'):
                            if(player1data[0] != '1'):
                                http_response = Requestapp(filename, "winner=0").getResponse()

                        #if player 1 and player 2 both made choices
                        if(player1data[1] is not '0' and player2data[1] is not '0'):
                            winner = getWinner(data['room'])
                            http_response = Requestapp(filename, "winner="+str(winner)).getResponse()
                        else:
                            http_response = Requestapp(filename, "winner=0").getResponse()

                    #update player data with their choice
                    elif(filename == "/reply"):
                            roomdata = io.open('./data/'+data['room']+'/'+data['player'], 'w+', encoding='utf8')
                            roomdata.write(u'2,'+data['item']+'\n')
                            roomdata.close()

                            http_response = Requestapp(filename, "").getResponse()

                    #when player leaves, a request is made to 'empty' file
                    elif(filename == "/playerleaves"):
                        roomdata = io.open('./data/'+data['room']+'/'+data['player'], 'w+', encoding='utf8')
                        roomdata.write(u'0,'+data['item']+'\n')
                        roomdata.close()

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
                print e
                http_response = Requestapp("", "", 404).getResponse()

            client_connection.sendall(http_response)
            client_connection.close()
            inputW.remove(client_connection)
