from socket import *
import time
import threading

running = True
studentID = 13330793
# threading.Thread(target=loop1_10).start()

serverName = 'localhost'
serverPort = 14000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))  # Bind to the port serverPort on localhost
serverSocket.listen(10) # LISTEN FOR UP TO 10 CONNECTIONs
print('Server Setup Complete')

# # For UDP
# socketUDP = socket(AF_INET, SOCK_DGRAM)  # UDP uses datagrams, not a stream
# socketUDP.bind(('',serverPort))
# # UDP doesn't need to establish a back and forth connection to verify message integrity,
# # hence why there is no listen method used

# HELO function
def heloFunction(inputMessage, conn):
    print("Received HELO")
    localAddressIP = gethostbyname(getfqdn())  # RETURNS INCORRECT IP ADDRESS FOR EXTERNAL USE
    helo_reply = "HELO{}IP:{}\nPort:{}\nStudentID:{}\n".format(inputMessage[4:],localAddressIP,serverPort,studentID)     
    conn.send(helo_reply.encode())
    print("Sent Reply {}".format(helo_reply))


# Join chatroom function
def joinChatroom(inputMessage, conn):
    # INCLUDE CODE TO JOIN A CHATROOM (ADD TO A CHATROOM LIST VIA MUTEX)
    join_text_split = inputMessage.splitlines()  # splits message by newlines
    join_room_name = join_text_split[0][15:]  # First line with "JOIN_CHATROOM: " cut off
    join_client_ip = join_text_split[1][11:]  # Second line with "CLIENT_IP: " cut off
    join_port = join_text_split[2][6:]  # Third line with "PORT: " cut off
    join_client_name = join_text_split[0][13:]  # Fourth line with "CLIENT_NAME: " cut off

    room_number = 0  # replace with correct room numbering system
    client_number = 0  # replace with correct client numbering system
    join_text_response = "JOINED_CHATROOM: {}\nSERVER_IP: {}\nPORT: {}\nROOM_REF: {}\nJOIN_ID: {}\n".format(join_room_name, gethostbyname(getfqdn()), join_port, room_number, client_number)
    print(join_text_response.encode())
    conn.send(join_text_response.encode())



def receive_clients(conn):
    # TELNET SENDS MESSAGES WITH '\r\n' AT THE END. CHANGE TO '\n' FOR FINAL IMPLEMENTATION
    while 1:
        receivedMessage = conn.recv(1024)  # Read data from socket
        print("Byte String:")
        print(receivedMessage)  # incoming data is of byte type? (b'Text')
        print("------------")
        receivedMessage = receivedMessage.decode()  # decode from byte type to string type
        print(receivedMessage)
        print("------------")

	# HANDLING INPUT
	
        if receivedMessage[:4] == "HELO":  # Check if first 4 chars are HELO
            heloFunction(receivedMessage, conn)

        elif receivedMessage[:13] == "JOIN_CHATROOM":
            joinChatroom(receivedMessage, conn)

        elif receivedMessage == "KILL_SERVICE\n":  # When telnet leaves, it sends blank data. Replace with end message
            break
        #else:
        #    print("INVALID INPUT DETECTED")
            
    print("Ended connection")
    conn.close()  # Close the socket


while running:
    connectionSocket, addr = serverSocket.accept()
    print('Received Connection')
    threading.Thread(target=receive_clients, args=(connectionSocket,)).start()

    

