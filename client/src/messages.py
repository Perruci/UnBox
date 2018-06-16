""" Package which hosts message types for recieving and sending

Its supposed to be a shared package between clients and server.

"""

def send_text(phrase):
    """ Format text messages and return its bytes """
    return bytes(phrase,'UTF-8')

def recieve_text(data):
    """ Recieves a binary data and returns string message

    Data: binary value eg. csocket.recv(2048)

    """
    return data.decode()

def end_connection():
    """ Format message to terminate socket connection with server """
    return send_text('bye')
