""" Package which hosts message types for recieving and sending """

def send_text(phrase):
    return bytes(phrase,'UTF-8')
