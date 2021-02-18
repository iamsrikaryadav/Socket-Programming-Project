#reference for day 1: https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
#reference for day 2: https://gist.github.com/joaoventura/824cbb501b8585f7c61bd54fec42f08f
import os
import socket
'''
*******************************************************************************************************************************************
'''
# Define socket host and port
SERVER_HOST = '192.168.1.3'
SERVER_PORT = 8888

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

'''
*******************************************************************************************************************************************
'''
def handle_request(request):
    #Handles the HTTP request.
    headers = request.split('\n')
    # extracting the content from http://192.168.1.3:8888/index.html which is after http://192.168.1.3:8888
    filename = headers[0].split()[1]
    #If only slash(/) provided after domain we are returning the index.html content.
    url=r'D:\2020501062\Computer Networking\Project\htmldocs'
    # Defining root folder
    if filename=='/':
        return 'HTTP/1.0 200 OK\n\n' + server_request(url)
    if filename == '/':
        filename = '/index.html'
    
    url=url+'\\'+filename[1:]
    print(url)
    if os.path.isdir(url):
        print("True")
        return "HTTP/1.0 200 Ok\n\n"+server_request(url)

    try:
        #spliting the string with (.) dot to get extensions
        try:
            file_ext = filename.split(".")[1]
        except:
            file_ext="txt"
        # print(file_ext)

        if file_ext not in ["txt","html","jpg","pdf"]:
            return 'HTTP/1.0 415 Unsupported Media Type\n\nThe server will not accept the request, because the media type is not supported'

        if file_ext in ["jpg","pdf"]:
            fin = open('htmldocs' + filename,'rb')
            content = fin.read()
            fin.close()
            client_connection.sendall('HTTP/1.0 200 OK\n\n'.encode())
            client_connection.sendall(content)
            return ""
        

        fin = open('htmldocs' + filename,encoding='utf-8')
        content = fin.read()
        fin.close()
        
        response = 'HTTP/1.0 200 OK\n\n' + content
    
    except FileNotFoundError:
        response = 'HTTP/1.0 400 NOT FOUND\n\nFile Not Found'
    
    if filename == '/logfile.html':
        response = 'HTTP/1.0 403 Forbidden\n\nYou dont have permission to acesss this file on this server'

    return response
'''
*******************************************************************************************************************************************
'''

def server_request(url):
    content=""
    list_of_dir = os.listdir(url)
    for i in list_of_dir:
        content = content+ '<a href="http://192.168.1.3:8888/' + i +'">' + i +'</a><br>'
    # print(content) 
    return content

'''
*******************************************************************************************************************************************
'''
while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    # Return a HTTP response
    response = handle_request(request)
    client_connection.sendall(response.encode())

    #Close connection
    client_connection.close()

# Close socket
server_socket.close()