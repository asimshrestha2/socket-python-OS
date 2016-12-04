import socket
import os
import io
import time
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
            if( data['player'] == 1 ):
                roomdata2 = io.open('./data/'+data['room']+'/2', 'r', encoding='utf8')
                player2data = roomdata2.read()
                roomdata2.close()
                if(player2data[0] != 1):
                    http_response = Requestapp(filename, "winner=0").getResponse()

            #If player 2, check player 1 data file to check if theyre there
            elif(data['player'] == 2):
                roomdata1 = io.open('./data/'+data['room']+'/1', 'r', encoding='utf8')
                player1data = roomdata2.read()
                roomdata1.close()
                if(player1data[0] != 1):
                    http_response = Requestapp(filename, "winner=0").getResponse()

                    roomdata1 = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8')
                    roomdata2 = io.open('./data/'+data['room']+'/2', 'w+', encoding='utf8')
                    player1data = roomdata1.read()
                    player2data = roomdata2.read()
                    roomdata1.close()
                    roomdata2.close()

                #if player 1 and player 2 both made choices
                if(player1data[2] > 0 and player2data[2] > 0):
                    winner = getWinner(room['data'])
                    http_response = Requestapp(filename, "winner="+winner).getResponse()

                else:
                    http_response = Requestapp(filename, "Both players need to make a choice").getResponse()

        #update player data with their choice
        elif(filename == "/reply"):
                roomdata = io.open('./data/'+data['room']+'/'+data['player'], 'w+', encoding='utf8')
                roomdata.write(u'2,'+data['item']+'\n')
                roomdata.close()

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

#Accesses both player data files, and returns either 1 or 2 for which player won
def getWinner(roomnum):
    return 1
