#reference for day 1: https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
#reference for day 2: https://gist.github.com/joaoventura/824cbb501b8585f7c61bd54fec42f08f

import socket
# import requests

# r = requests.head('http://192.168.1.3:8888//', data ={'key':'value'}) 
# print(r)
# print(r.headers)
# print(r.content)

# Define socket host and port
SERVER_HOST = '192.168.1.3'
SERVER_PORT = 8888

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

def handle_request(request):
    #Handles the HTTP request.
    headers = request.split('\n')
    # print(headers[0].split())
    filename = headers[0].split()[1]

    if filename == '/':
        filename = '/index.html'

    try:
        try:
            file_ext = filename.split(".")[1]
        except:
            file_ext="txt"
        # print(file_ext)
        if file_ext not in ["txt","html"]:
            return 'HTTP/1.0 415 Unsupported Media Type\n\nThe server will not accept the request, because the media type is not supported'
        fin = open('htmldocs' + filename,encoding='utf-8')
        content = fin.read()
        fin.close()
        
        response = 'HTTP/1.0 200 OK\n\n' + content
    

    except FileNotFoundError:
        response = 'HTTP/1.0 400 NOT FOUND\n\nFile Not Found'
    
    if filename == '/logfile.html':
        response = 'HTTP/1.0 403 Forbidden\n\nYou dont have permission to acesss this file on this server'


    return response


while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    # Get the content of htdocs/index.html
    # fin = open('aboutme.html')
    # content = fin.read()
    # fin.close()

    # Send HTTP response
    # response = 'HTTP/1.0 200 OK\n\n'+ content
    response = handle_request(request)
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()