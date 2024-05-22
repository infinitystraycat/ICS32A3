# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME
# EMAIL
# STUDENT ID
import socket
import threading
import ds_protocol as protocol
import json
#import requests

PORT = 3021
HOST = '168.235.86.101'
TIMESTAMP = "1603167689.3928561"
#Test server code here
#PORT = 2024
#HOST = "127.0.0.1"

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    #TODO: return either True or False depending on results of required operation
    try:
        print(message)
        if len(message) < 1: 
            print('ERROR: You can not upload a blank post')
            return False
        if len(bio) < 1: 
            print('ERROR: You can not upload a blank bio')
            return False
        
        client = connect(server)
        send = client.makefile('w')
        recv = client.makefile('r')
        
        token = join_as_user(client, username, password)
        post = {"token":token, "post": {"entry": message, "timestamp": TIMESTAMP}}
        send.write(json.dumps(post) + '\r\n')
        send.flush()
        resp = recv.readline()
        print('resp: ' + resp)

        if bio:
            cbio = {"token":token, "bio": {"entry": bio, "timestamp": TIMESTAMP}}
            send.write(json.dumps(cbio) + '\r\n')
            send.flush()
        
        client.close()
        
        return True
    except Exception as e: 
        print('Error as: ' + str(e))
        print('No proper input given. Please check your inputs.')
        return False

# Define the main method for the client
def main():
    send(HOST, PORT, "may", "pwd", "here is my new final post", "funny bio")

def make_post():
    entry = input('What would you like your post entry to be? \n')
    post = {"entry": entry, "timestamp": TIMESTAMP}
    return post

def c_bio():
    bio = input('What would you like your bio to be? \n')
    bio_c = {"entry": bio, "timestamp": TIMESTAMP}
    return bio_c

def join_as_user(client, usr, pwd):
    '''
    Logs in using the provided username and password,
    and returns a token. 
    '''
    join_msg = {"join": {"username": usr,"password": pwd, "token":""}}
        
    send = client.makefile('w')
    recv = client.makefile('r')
    send.write(json.dumps(join_msg) + '\r\n')
    send.flush()

    resp = recv.readline()
    print('resp: ' + resp)
    updated = json.loads(resp)
    token = updated["response"]['token']
    return token


def connect(host):
    try:
        server_address = (host, PORT)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        print('connect successful')
        
        return client_socket
    
    except Exception as e:
        print('error')
        print(e)
    

if __name__ == "__main__":
    main()
    #socket = connect()
    