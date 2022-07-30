# HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants


# TO DO: import modules


# TO DO: set constants
import os
import socket

SOCKET_TIMEOUT = 60
IP = "127.0.0.1"
PORT = 80
DEFAULT_URL = 'index.html'

def calculate_area(url):
    url2 = url[:url.find("=") + 1]
    num1 = url[url.find("=") + 1:]
    url3 = num1
    num1 = num1[:num1.find("&")]
    url3 = url3[url3.find("&"):]
    num2 = url3[url3.find("=") + 1:]
    return (float(num1) * float(num2)) / 2


def calculate_next(url):
    num = int(url[url.find("=") + 1:])
    return num + 1


def get_file_data(filename):
    if os.path.exists(filename):
        file = open(filename, 'rb')
        data = file.read()
        file.close()
    else:
        return ""
    return data


def handle_client_request(resource, client_socket):
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    url = resource
    if "/calculate-area?height=" in resource:
        file = open(r"C:\temp\webroot\file2.html", 'wb')
        file.write(bytes("<html>".encode()))
        file.write(bytes("<body>".encode()))
        file.write(bytes("<p>".encode() + str(calculate_area(resource)).encode() + "</p>".encode()))
        file.write(bytes("</body>".encode()))
        file.write(bytes("</html>".encode()))
        client_socket.send(r"C:\temp\webroot\file2.html".encode())
        file.close()
    if "/calculate-next?num=" in resource:
        file = open(r"C:\temp\webroot\file.html", 'wb')
        file.write(bytes("<html>".encode()))
        file.write(bytes("<body>".encode()))
        file.write(bytes("<p>".encode() + str(calculate_next(resource)).encode() + "</p>".encode()))
        file.write(bytes("</body>".encode()))
        file.write(bytes("</html>".encode()))
        client_socket.send(r"C:\temp\webroot\file.html".encode())
        file.close()
    elif resource == '':
        url = DEFAULT_URL
    elif resource != '':
        url = resource
    else:
        if not os.path.exists(url):
            http_response = r"HTTP/1.0 404 Not Found\r\n"
            client_socket.send(http_response.encode())

    # TO DO: extract requested file tupe from URL (html, jpg etc)

    filetype = resource.split(".")[-1]
    print(filetype)
    http_header = r'HTTP/1.1 200 OK \r\n'
    filename = url
    print(filename)

    if filetype == 'html':
        http_header = http_header + r'Content-Type: text/html; charset=utf-8\r\n'  # TO DO: generate proper HTTP header
    elif filetype == 'jpg':
        http_header = http_header + r'Content-Type: image/jpeg/\r\n'  # TO DO: generate proper jpg header
    elif filetype == 'js':
        http_header = http_header + r"Content-Type: text/javascript; charset=UTF-8\r\n"
    elif filetype == 'css':
        http_header = http_header + r"Content-Type: text/css\r\n"
    # TO DO: handle all other headers

    # TO DO: read the data from the file
    print(filename)


    client_socket.send(r"C:\temp\webroot\index.html".encode())

    print("Server stopped.")
    if filetype == 'html' or filetype == 'css' or filetype == 'js' or filetype == 'jpg':
        data = get_file_data(filename)
        http_response = http_header + data.decode()
        print(http_response)


def validate_http_request_cal_area(request):
    # """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    get_check = request[:request.find(" ")]
    request = request[len(get_check) + 1:]
    url1 = request[:request.find(" ")]
    url2 = url1[:url1.find("=") + 1]
    num1 = url1[url1.find("=") + 1:]
    url3 = num1
    num1 = num1[:num1.find("&")]
    url3 = url3[url3.find("&"):]
    num2 = url3[url3.find("=") + 1:]
    request = request[len(url1) + len(get_check) - 2:]
    isHTTP = request[:request.find(r'\r')]
    request = request[request.find(".1") + 2:]
    end = request
    if get_check == "GET" and url2 + num1 + url3 == url1 and len(num1) > 0 and len(num2) > 0 and isHTTP == "HTTP/1.1"\
            and end == r'\r\n':
        return True, url1
    else:
        return False, None


def validate_http_request_cal(request):
    # """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    print(type(request))
    get_check = request[:request.find(" ")]
    request = request[len(get_check) + 1:]
    url = request[:request.find(" ")]
    num = url[url.find("=") + 1:]
    request = request[len(url) + len(get_check) - 2:]
    isHTTP = request[:request.find(r'\r')]
    request = request[request.find(".1") + 2:]
    end = request
    if get_check == "GET" and url == "/calculate-next?num=" + num and isHTTP == "HTTP/1.1" and end == r'\r\n':
        return True, url
    else:
        return False, None


def validate_http_request(request):
    # """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    print(type(request))
    get_check = request[:request.find(" ")]
    request = request[len(get_check) + 1:]
    url = request[:request.find(" ")]
    request = request[len(url) + len(get_check) - 2:]
    isHTTP = request[:request.find(r'\r')]
    request = request[request.find(".1") + 2:]
    end = request
    if get_check == "GET" and os.path.exists(url) and isHTTP == "HTTP/1.1" and end == r'\r\n':
        return True, url
    else:
        return False, None


def handle_client(client_socket):
    print('Client connected')
    while True:
        # TO DO: insert code that receives client request
        client_request = client_socket.recv(1024).decode()
        if "/calculate-next?num=" in client_request:
            valid_http, resource = validate_http_request_cal(client_request)
        elif "/calculate-area?" in client_request:
            valid_http, resource = validate_http_request_cal_area(client_request)
        else:
            valid_http, resource = validate_http_request(client_request)
        if client_socket == "EXIT":
            break
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
        else:
            print('Error: Not a valid HTTP request')
            break
    print('Closing connection')
    client_socket.send("Bye".encode())
    client_socket.close()
    return resource


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
    print("Listening for connections on port %d" % PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == '__main__':
    main()
