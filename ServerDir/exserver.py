from socket import *
import os
import threading

# specify ip address and port number for server
serverIp = "localhost"
serverPort = 13002

# Creating Socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# binding port_number to socket
serverSocket.bind((serverIp, serverPort))

# listening for client
serverSocket.listen(50)
print("Server Listening on {}:{}".format(serverIp, serverPort))

# printing message so user can understand that server is ready to listen
print("The server is ready to receive")


# method for handle client connection
def handle_client_connection(client_socket, request, filename, userinput, file):

    print("Received {}".format(request))

    if userinput == "get":
        if os.path.exists(filename):
            f1 = open(os.getcwd() + "/" + filename, "rb")
            data = f1.read()
            client_socket.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n".encode() + data)
            print("Data successfully send")
        else:
            client_socket.sendall("404 not found!!".encode())
            print("404 not found!!")
        client_socket.close()

    elif userinput == "put":
        print("put")
        f1 = open(filename, "wb")
        f1.write(file)
        client_socket.send("File successfully uploded!!".encode())
        client_socket.close()

    elif userinput == "head":
        print("head")
        if os.path.exists(filename):
            f1 = open(os.getcwd() + "/" + filename, "rb")
            data = f1.read()
            head_data = data.split("</head>".encode())
            client_socket.sendall(
                "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n".encode() + head_data[0] + "\n</head>".encode())
            print("Data successfully send")
        else:
            client_socket.sendall("404 not found!!".encode())
            print("404 not found!!")
        client_socket.close()

    elif userinput == "delete":
        print("delete")
        if os.path.exists(filename):
            os.remove(filename)
            if os.path.exists(filename):
                print("Not Successfull")
                client_socket.sendall("Not Successfull".encode())
            else:
                print("Successfully deleted!!")
                client_socket.sendall("Successfully deleted!!".encode())
        else:
            print("File not found!!")
            client_socket.sendall("File not found!!".encode())
        client_socket.close()

    else:
        print("Invalid user input!!")
        client_socket.close()


while True:
    # here server accept the client and store address of client in addr and message in connectionSocket
    client_socket, addr = serverSocket.accept()
    request = client_socket.recv(10244)
    print("Accepted connection from {}:{}".format(addr[0], addr[1]))

    # Here logic for checking request coming from browser or client
    new_strr = request.decode().splitlines()[0]
    strr = new_strr.split(" ")
    userInput = strr[0].lower()

    if userInput == "get" or userInput == "head":
        v = strr[2].split("/")
        httpVersion = v[1]
        fileName = "index.html"
        file = "tcpclient.py"
    else:
        file, fileName, userInput, httpVersion = [str(i) for i in request.decode('utf-8').split('||')]

    if httpVersion == "1.0":

        print("HTTP VERSION 1.0")
        handle_client_connection(client_socket, request, fileName, userInput, file.encode())

    else:
        print("HTTP VERSION 1.1")
        client_handler = threading.Thread(
            target=handle_client_connection, args=(client_socket, request, fileName, userInput, file.encode())
        )
        client_handler.start()
