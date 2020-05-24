from socket import *
import sys

# give server name as localhost

# command line arguments
client_name = sys.argv[0]
serverName = sys.argv[1]
clientPort = int(sys.argv[2])
httpVersion = sys.argv[3]


# creating socket for send message to server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, clientPort))

# Taking input from user
print("\n\nEnter PUT, GET, HEAD, DELETE: \n")
userInput = input()
userInput.lower()

# specify file name on which we do all operation
filename = "index.html"

# Open and read file
myFile = open("/Users/kavanpatel/Desktop/CS537/ClientDir/" + filename, "rb")
myText = myFile.read().decode()

# Logic for all operations
if userInput == "put":
    # Upload file to server
    clientSocket.sendall(str.encode("||".join([myText, filename, userInput, httpVersion, ])))
    print("Message from server : ".encode() + clientSocket.recv(1024))

elif userInput == "get":

    # GET file from server and display
    clientSocket.sendall(str.encode("||".join([myText, filename, userInput, httpVersion, ])))
    response = clientSocket.recv(10244)
    print(response.decode())

elif userInput == "head":
    # GET header file of html file and display
    clientSocket.sendall(str.encode("||".join([myText, filename, userInput, httpVersion, ])))
    response = clientSocket.recv(10244)
    print(response.decode())

elif userInput == "delete":
    # DELETE File from server
    filenamee = input("Enter file name which you want to delete : ")
    clientSocket.sendall(str.encode("||".join([myText, filenamee, userInput, httpVersion, ])))
    response = clientSocket.recv(1024)
    print(response.decode())

else:
    # Other input
    clientSocket.sendall(str.encode("||".join([myText, filename, userInput, httpVersion, ])))
    print("Error Type again")
