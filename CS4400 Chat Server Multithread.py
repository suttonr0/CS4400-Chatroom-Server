from socket import *
import time
import threading

running = True
studentID = 13330793


roomMutex = threading.Lock()
roomNameToRef = {}  # Dictionary with room names as keys, and room refs as values ( ROOM IDENTIFICATION BY NAME )
               # Each room will be a list of connections to the clients in that room 
roomRefToConn = {}  # Dictionary which takes room ref and returns list of connections ( STORES CONNECTIONS OF ROOM ROOM_REF )
roomRefCount = 0  # Value used to assign a unique room reference to each room
connToJoinID = {}  # keys are conn, values are the associated client Join_ID ( CLIENT IDENTIFICATION BY CONNECTION )
joinIDCount = 0  # counter for Join_ID assignment

serverName = 'localhost'
serverPort = 14000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))  # Bind to the port serverPort on localhost
serverSocket.listen(10) # LISTEN FOR UP TO 10 CONNECTIONs
print('Server Setup Complete')

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
    text_split = inputMessage.splitlines()  # splits message by newlines
    room_name = text_split[0][15:]  # First line with "JOIN_CHATROOM: " cut off
    client_ip = text_split[1][11:]  # Second line with "CLIENT_IP: " cut off
    port = text_split[2][6:]  # Third line with "PORT: " cut off
    client_name = text_split[3][13:]  # Fourth line with "CLIENT_NAME: " cut off
    
    # Global keyword needed to use the variables created outside this function
    global roomMutex
    global roomNameToRef
    global roomRefToConn
    global roomRefCount
    global connToJoinID
    global joinIDCount    

    # Joining the chatroom and creating one if there isn't one
    roomMutex.acquire()
    if room_name not in roomNameToRef:  # Check if the room already exists
                                        # If not then assign a Room_Ref number to the room name
        roomRefCount += 1  # Increment room reference counter
        roomNameToRef[room_name] = roomRefCount  # associate the room name with a room reference
        roomRefToConn[roomRefCount] =  list()  # create a list for connections for that room_ref
    currentRoomRef = roomNameToRef[room_name]  # Get room ref from room name
    roomRefToConn[currentRoomRef].append(conn)  # Add connection to list
                                              # Access the connection list by room_ref through roomRefToConn dictionary
    # Check if already in room before adding conn??
    roomMutex.release()
    
    if conn not in connToJoinID:  # If the current client isn't in the client list
        joinIDCount += 1
        connToJoinID[conn] = joinIDCount  # Give the client a joinID to be referenced by its conn 
    client_joinID = connToJoinID[conn]

    text_response = "JOINED_CHATROOM: {}\nSERVER_IP: {}\nPORT: {}\nROOM_REF: {}\nJOIN_ID: {}\n".format(room_name, gethostbyname(getfqdn()), port, currentRoomRef, client_joinID)
    print(text_response.encode())
    conn.send(text_response.encode())

    room_response = "CHAT: {}\nCLIENT_NAME: {}\nMESSAGE: {} has joined this chatroom\n\n".format(currentRoomRef, client_name, client_name)

    # Send message to all clients in room that a new client has joined
    for connect in roomRefToConn[currentRoomRef]:
        connect.send(room_response.encode())


def leaveChatroom(inputMessage, conn):
    # INCLUDE CODE TO JOIN A CHATROOM (ADD TO A CHATROOM LIST VIA MUTEX)
    text_split = inputMessage.splitlines()  # splits message by newlines
    room_ref = text_split[0][16:]  # First line with "LEAVE_CHATROOM: " cut off
    join_ID = text_split[1][9:]  # Second line with "JOIN_ID: " cut off
    client_name = text_split[2][13:]  # Fourth line with "CLIENT_NAME: " cut off
    
    global roomMutex
    global roomRefToConn
    global connToJoinID
    global joinIDCount  

    if conn in roomRefToConn[int(room_ref)]:  # Removes connection from room list
        roomRefToConn[int(room_ref)].remove(conn)
    leave_response = "LEFT_CHATROOM: {}\nJOIN_ID: {}\n".format(room_ref, join_ID)
    conn.send(leave_response.encode())  # Tell client that they have left

    room_response = "CHAT: {}\nCLIENT_NAME: {}\nMESSAGE: {} has left this chatroom\n\n".format(room_ref, client_name, client_name)  # Message saying that the client has left

    conn.send(room_response.encode())  # Send message to client who has just left the room

    # Send message to all clients in room that the client has left
    for connect in roomRefToConn[int(room_ref)]:
        connect.send(room_response.encode())


def chatToChatroom(inputMessage, conn):
    # INCLUDE CODE TO JOIN A CHATROOM (ADD TO A CHATROOM LIST VIA MUTEX)
    text_split = inputMessage.splitlines()  # splits message by newlines
    room_ref = text_split[0][6:]  # First line with "CHAT: " cut off
    join_ID = text_split[1][9:]  # Second line with "JOIN_ID: " cut off
    client_name = text_split[2][13:]  # Third line with "CLIENT_NAME: " cut off
    chatMessage = text_split[3][9:]  # Fourth line with "MESSAGE: " cut off
    
    room_response = "CHAT: {}\nCLIENT_NAME: {}\nMESSAGE: {}\n\n".format(room_ref, client_name, chatMessage)

    # Send message to all clients in room
    for connect in roomRefToConn[int(room_ref)]:
        connect.send(room_response.encode())


#  This function decides what to do with the contents received from the client connection
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

        elif receivedMessage[:14] == "LEAVE_CHATROOM":
            leaveChatroom(receivedMessage, conn)

        elif receivedMessage[:4] == "CHAT":
            chatToChatroom(receivedMessage, conn)

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

    

