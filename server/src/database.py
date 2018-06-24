""" Database module for UnBox application """

import os
import ruamel.yaml as yaml
import pathlib

USER_AUTH_FILE = 'server/user_data.yaml'

def create_dir(directory_path):
    """ Creates a directory if it doesnt exist """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

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

def load_user_data(username):
    """ Returns user data stored on USER_AUTH_FILE """
    data = load_yaml(USER_AUTH_FILE)
    return data.get(username)

def update_user_data(username, new_dict):
    """ Updates stored user data with new_dict """
    data = load_yaml(USER_AUTH_FILE)
    data[username] = new_dict
    dump_yaml(USER_AUTH_FILE, data)


def add_user_filesystem(username, path_to_file, file_size):
    """ Adds a new file on user data """
    new_file = {path_to_file : file_size}
    user_dict = load_user_data(username)

    if 'files' not in user_dict:
        user_dict['files'] = new_file
    else:
        files_dict = user_dict['files']
        files_dict.update(new_file)
        user_dict['files'] = files_dict
    print('Updating {} filesystem'.format(username))
    update_user_data(username, user_dict)

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
