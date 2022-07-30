import socket
import webbrowser

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 80))
data = ""
while data != "Bye":
    msg = input("Please enter HTTP GET request\n")
    my_socket.send(msg.encode())
    data = my_socket.recv(1024).decode()
    print(data)
    if data != "Bye":
        webbrowser.open(data)

my_socket.close()

