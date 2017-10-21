from socket import *
import time
import threading

running = True

# threading.Thread(target=loop1_10).start()

serverName = 'localhost'
serverPort = 14000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))  # Bind to the port
serverSocket.listen(1) # LISTEN FOR 1 CONNECTION
print('Server Setup Complete')

connectionSocket, addr = serverSocket.accept()
print('Received Connection')

while running:
    receivedMessage = connectionSocket.recv(1024)  # Read data from socket
    print("Byte String:")
    print(receivedMessage)  # incoming data is of byte type? (b'Text')

    receivedMessage = receivedMessage.decode()  # decode from byte type to string type
    print("String:")
    if receivedMessage == "hi\r\n":  # Sending "hi" by telnet sends "hi\r\n"
        print("matched")
    print(receivedMessage)
    if receivedMessage == '':  # When telnet leaves, it sends blank data. Replace with end message
        break
print("Ended connection")
connectionSocket.close()  # Close the socket

