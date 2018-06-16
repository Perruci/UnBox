""" Package which hosts message types for recieving and sending """

def send_text(phrase):
    """ Format text messages and return its bytes """
    return bytes(phrase,'UTF-8')

def end_connection():
    """ Format message to terminate socket connection with server """
    return send_text('bye')
