""" Database module for UnBox application """

import ruamel.yaml as yaml
import pathlib

USER_AUTH_FILE = 'server/user_data.yaml'

def file_exists(file_path):
    """ Returns true if file exists, false if it doesnt """
    file = pathlib.Path(file_path)
    return file.is_file()

def load_yaml(file_path):
    """ Loads YAML file and returns its data as a dictionary """
    with open(file_path, 'r') as usernames_yaml:
        try:
            data = yaml.safe_load(usernames_yaml)
        except yaml.YAMLError as exc:
            print(exc)
    return data

def dump_yaml(file_path, data):
    """ Writes data to a YAML file and replaces its contents"""
    with open(file_path, 'w+') as usernames_yaml:
        yaml.dump(data, usernames_yaml)

def register_user(username, password):
    """ Append new username to USER_AUTH_FILE """
    new_user_data = {username : {'password' : password}}
    if file_exists(USER_AUTH_FILE):
        # Reads whole file and then updates it
        data = load_yaml(USER_AUTH_FILE)
        data.update(new_user_data)
        dump_yaml(USER_AUTH_FILE, data)
    else:
        # create new file
        data = new_user_data
        dump_yaml(USER_AUTH_FILE, data)

def authenticate_user(username, password):
    """ Verify if user is listed on USER_AUTH_FILE
    return:
    Boolean tuple (user_exists, password_correct)
    """
    user_exists, password_correct = False, False

    if not file_exists(USER_AUTH_FILE):
        return user_exists, password_correct

    data = load_yaml(USER_AUTH_FILE)

    if username in data:
         """ Checks for username as a key in database """
         user_exists = True
         if data[username]['password'] == password:
            password_correct = True

    return user_exists, password_correct
