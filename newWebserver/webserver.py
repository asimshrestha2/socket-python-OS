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

        elif (protocal[0] == "POST"):
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

<<<<<<< HEAD
		    #make player 1 data file
                    roomdata = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8') 
                    roomdata.write(u'1,0\n')
		    roomdata.close()

		    #make player 2 data file
=======
		#checks if room exists and creates directory, and also creates player data.
                if not os.path.exists('./data/'+data['room']):
                    newfile = True
                    os.makedirs('./data/'+data['room'])

		    #[0-1],[0-3] first number is 'is there' bit, and second number is 0 for not chosen and 1-3 for rock/paper/scissors
		    #creates player 1 and 2 data, player 1 first value is set to 1 for "is there"
		    #w+ opens for reading and writing and creates file if it doesnt exist
                    roomdata = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8')
                    roomdata.write(u'1,0\n')
        		    roomdata.close()
>>>>>>> d016f25159b9dea25620c860051aa13a2d4e3e21
                    roomdata = io.open('./data/'+data['room']+'/2', 'w+', encoding='utf8')
                    roomdata.write(u'0,0\n')
        		    roomdata.close()

		    #respond that theyre player 1
		    http_response = Requestapp(filename, "player=1").getResponse()
<<<<<<< HEAD
		    client_connection.sendall(http_response)
		    client_connection.close()

		else: #if room does exist
		    roomdata1 = io.open('./data/'+data['room']+'/1', 'r', encoding='utf8')
		    roomdata2 = io.open('./data/'+data['room']+'/2', 'r', encoding='utf8')
		    player1data = roomdata1.read()
		    player2data = roomdata2.read()
		    roomdata1.close()
		    roomdata2.close()

		    #if only player 2 is in the room
		    if((player1data[0] == 0 and player2data[0] == 1)):
                    	roomdata = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8')
                    	roomdata.write(u'1,0\n')
		    	roomdata.close()
			#at this point, both players are now in the room

		    	http_response = Requestapp(filename, "player=1").getResponse()
		    	client_connection.sendall(http_response)
		    	client_connection.close()

		    #if only player 1 is in the room
		    elif(player2data[0] == 0 and player1data[0] == 1):
                    	roomdata = io.open('./data/'+data['room']+'/2', 'w+', encoding='utf8')
                    	roomdata.write(u'1,0\n')
		    	roomdata.close()
			#at this point, both players are now in the room

		    	http_response = Requestapp(filename, "player=2").getResponse()
		    	client_connection.sendall(http_response)
		    	client_connection.close()

		    elif(player2data[0] == 1 and player1data[0] == 1):
			#room is full
		    	http_response = Requestapp(filename, "Room is Full.").getResponse()
		    	client_connection.sendall(http_response)
		    	client_connection.close()
			

	    elif(filename == "/update"):
		if( data['player'] == 1 ):
		    #If player 1, check player 2 data file to check if theyre there
		    roomdata2 = io.open('./data/'+data['room']+'/2', 'r', encoding='utf8')
		    player2data = roomdata2.read()
		    roomdata2.close()
		    if(player2data[0] != 1):
			http_response = Requestapp(filename, "winner=0").getResponse()
		    	client_connection.sendall(http_response)
		    	client_connection.close()

		elif(data['player'] == 2):
		    #If player 1, check player 2 data file to check if theyre there
		    roomdata1 = io.open('./data/'+data['room']+'/1', 'r', encoding='utf8')
		    player1data = roomdata2.read()
		    roomdata1.close()
		    if(player1data[0] != 1):
			http_response = Requestapp(filename, "winner=0").getResponse()
		    	client_connection.sendall(http_response)
		    	client_connection.close()

		    roomdata1 = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8')
		    roomdata2 = io.open('./data/'+data['room']+'/2', 'w+', encoding='utf8')
		    player1data = roomdata1.read()
		    player2data = roomdata2.read()
		    roomdata1.close()
		    roomdata2.close()

		    if(player1data[2] > 0 and player2data[2] > 0):
		        winner = getWinner(room['data'])
		        http_response = Requestapp(filename, "winner="+winner).getResponse()
		        client_connection.sendall(http_response)
		        client_connection.close()
		    else:
		        http_response = Requestapp(filename, "Both players need to make a choice").getResponse()
		        client_connection.sendall(http_response)
		        client_connection.close()
		
	    elif(filename == "/reply"):
                roomdata = io.open('./data/'+data['room']+'/'+data['player'], 'w+', encoding='utf8') 
                roomdata.write(u'2,'+data['item']+'\n')
		roomdata.close()

	    elif(filename == "/playerleaves"):
		roomdata = io.open('./data/'+data['room']+'/'+data['player'], 'w+', encoding='utf8') 
                roomdata.write(u'0,'+data['item']+'\n')
		roomdata.close()
=======

		elif: #Gets here only if room exists

		    #If the request has item (the user's choice) and player number that's over than 0, then add choice data in for that player
		    if(data['item'] > 0 and data['player'] > 0 )
			roomdata = io.open('./data/'+data['room']+'/'+data['player'], 'w+', encoding='utf8')

		    	with io.open('./data/'+data['room']+'/'+data['player'], 'r', encoding='utf8') as roomdata #opens as read-only
		    	roomdata.write(u'1,' + data['item'] + '\n') #puts 1,[1-3] in file. If player made a choice, then they have to be in the room ex. 1,2
			roomdata.close()

		    else:
			#if room exists and choice is 0 and player is 0, then they are player 2. Send response data "player=2" for Javascript to retreive and use in next request
			http_response = Requestapp(filename, "player=2").getResponse()
			client_connection.sendall(http_response)
			client_connection.close()

		    if(data['room'] > 0 and data['player'] > 0):

			#gather player data for each player for checking if two players are in a room
		    	roomdata1 = io.open('./data/'+data['room']+'/1', 'r', encoding='utf8')
		    	roomdata2 = io.open('./data/'+data['room']+'/2', 'r', encoding='utf8')
		    	player1data = roomdata1.read()
		    	player2data = roomdata2.read()
		    	roomdata1.close()
		    	roomdata2.close()

			count = 0
		    	#checks if there are two players in the room, every second
		    	while(player1data[0] != 1 and player1data[0] != 1 and count != 10)
			    print("Waiting for two players...")
			    time.sleep(3) #sleeps for 3 second
		    	    roomdata1 = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8')
		    	    roomdata2 = io.open('./data/'+data['room']+'/2', 'w+', encoding='utf8')
		    	    player1data = roomdata1.read()
		    	    player2data = roomdata2.read()
			    roomdata1.close()
			    roomdata2.close()
			    count++;

			#if count equals 10, then there's a timeout
			if(count == 10):
			    http_response = Requestapp(filename, "Could not find player in time. 30 second timeout\n").getResponse()
			    client_connection.sendall(http_response)
			    client_connection.close()
			else:
			    #gather player data for each player for checking if each player made a choice
		    	    roomdata1 = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8')
		    	    roomdata2 = io.open('./data/'+data['room']+'/2', 'w+', encoding='utf8')
		    	    player1data = roomdata1.read()
		    	    player2data = roomdata2.read()
			    roomdata1.close()
			    roomdata2.close()

		    	    #checks every second if two players have made their choices, waits if not
		    	    while(player1data[2] > 0 and player1data[2] > 0)
			        print("Waiting for two players...")
			        time.sleep(3) #sleeps for 3 second
		    	        roomdata1 = io.open('./data/'+data['room']+'/1', 'w+', encoding='utf8')
		    	        roomdata2 = io.open('./data/'+data['room']+'/2', 'w+', encoding='utf8')
		    	    	player1data = roomdata1.read()
		    	    	player2data = roomdata2.read()
			    	roomdata1.close()
			    	roomdata2.close()

		    	    #gets winner and sends which player won as a response
		    	    winner = findWinner(data['room'])
		    	    http_response = Requestapp(filename, "winner=" + winner ).getResponse()
		    	    client_connection.sendall(http_response)
		    	    client_connection.close()

>>>>>>> d016f25159b9dea25620c860051aa13a2d4e3e21

        elif (protocal[0] == "GET"):
            if(filename == "/"):
                rf = open('./serverfiles/index.html', 'r')
                filename = "/index.html"
            else:
                rf = open('./serverfiles' + filename, 'r')

            filecontent = rf.read()
	    rf.close()
            http_response = Requestapp(filename, filecontent).getResponse()
	    client_connection.sendall(http_response)
	    client_connection.close()

    except Exception as e:
        print e
        http_response = Requestapp("", "", 404).getResponse()
	client_connection.sendall(http_response)
	client_connection.close()

#Accesses both player data files, and returns either 1 or 2 for which player won
<<<<<<< HEAD
def getWinner(roomnum):
    return 1
	
=======
def findWinner(roomnum):
	return 1
>>>>>>> d016f25159b9dea25620c860051aa13a2d4e3e21
