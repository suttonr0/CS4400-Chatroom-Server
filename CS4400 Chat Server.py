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
serverSocket.listen(2) # LISTEN FOR 1 CONNECTION
print('Server Setup Complete')

# # For UDP
# socketUDP = socket(AF_INET, SOCK_DGRAM)  # UDP uses datagrams, not a stream
# socketUDP.bind(('',serverPort))
# # UDP doesn't need to establish a back and forth connection to verify message integrity,
# # hence why there is no listen method used

connectionSocket, addr = serverSocket.accept()
print('Received Connection')

while running:

    # TELNET SENDS MESSAGES WITH '\r\n' AT THE END. CHANGE TO '\n' FOR FINAL IMPLEMENTATION

    receivedMessage = connectionSocket.recv(1024)  # Read data from socket
    print("Byte String:")
    print(receivedMessage)  # incoming data is of byte type? (b'Text')
    print("------------")
    receivedMessage = receivedMessage.decode()  # decode from byte type to string type

    if receivedMessage == "HELO text\r\n":  # Send reply with IP and port number
        localAddressIP = gethostbyname(getfqdn())  # RETURNS INCORRECT IP ADDRESS FOR EXTERNAL USE
        connectionSocket.send(("HELO text\nIP:{}\nPort:{}\nStudentID:{}\n"
                               .format(localAddressIP,serverPort,studentID)).encode())
    print(receivedMessage)
    if receivedMessage == "KILL_SERVICE\r\n":  # When telnet leaves, it sends blank data. Replace with end message
        break
print("Ended connection")
connectionSocket.close()  # Close the socket

