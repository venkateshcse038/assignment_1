import re
import json
import string

# search and format functions

def check_id_in_file(ui_emailid):
    '''
    checks the given emailid string in file data (emailid_database.json)
    if no file data exists it creates one and checks the file again
    :param user_id: validated emailid string
    :return: True if present False if not present 'no data' if no file data exists
    '''
    try:
        with open('emailid_database.json', 'r+') as file:
            # First we load existing data into a dict.
            try:
                file_data = json.load(file)
            # checking if emailid already exists in the file
                if ui_emailid in file_data:
                    return True
                else:
                    return False
            except json.decoder.JSONDecodeError:
                return 'no_data'
    except FileNotFoundError:
        filecreation = open('emailid_database.json', 'a')
        filecreation.close()
        return check_id_in_file(ui_emailid)


def update_data(new_data=None, key=None, filename='emailid_database.json'):
    '''
    :function: it appends the file to file data if the parameter is new_data ,it updates the password if the parameter is key
    :param new_data: default = none,new_data (user entered valid emailid and password pair in dict format)
    :param key: default = none, key (emailid string to search in file data for its value (password)
    :param filename: emailid_database.json
    :return: none
    '''

    with open(filename, 'r+') as file:
        # appending a new file
        if new_data is not None:
            try:
                file_data = json.load(file)
                file_data.update(new_data)
                file.seek(0)
                json.dump(file_data, file)
        # adding the 1st file ever
            except json.decoder.JSONDecodeError:
                with open('emailid_database.json', 'a') as file2:
                    json.dump(new_data, file2)
        # changing the value(password) for the key(emailid)
        if key is not None:
            file_data = json.load(file)
            file_data[key] = check_passwordformat(input('Enter new password : '))
            file.seek(0)
            json.dump(file_data, file)

# format checking functions

def check_emailidformat(mailid):
    '''
    it checks if the emailid satisfies the format conditions
    1. '@' and '.' should be present
    2. should have some prefix to '@'
    3. '.' should not immediately follow '@'
    4. shouldn't start with spl.character or number
    :param mailid: user input emailid string
    :return: same user input emailid string if conditions are satisfied or
             calls the function recursively until its satisfied
    '''

    regex = r'[A-Za-z].+@[A-Za-z0-9-]+\.[A-Za-z]+'
    regex1 = r'[A-Za-z]+@[A-Za-z0-9-]+\.[A-Za-z]+'
    if re.fullmatch(regex, mailid):
        return mailid
    elif re.fullmatch(regex1, mailid):
        return mailid
    else:
        print("Invalid Email")
        check_emailidformat(input('Re-enter emailid : '))


def check_passwordformat(password):
    '''
    it checks if the password format conditions are satisfied
    1. length more than 16
    2 must contain
        2.1 one spl.charc
        2.2 one digit
        2.3 one uppercase
        2.4 one lowercase
    :param password: user input password
    :return: return the same user input password or calls the function recursively until its satisfied
    '''

    chars = set(string.punctuation)
    if 5 < len(password) > 16: # 1
        if any(i in chars for i in password): # 2.1
            if bool(re.search(r'\d', password)): # 2.2
                if bool(re.search(r'[A-Z]', password)): # 2.3
                    if bool(re.search(r'[a-z]', password)): # 2.4
                        return password
                else:
                    print('password should contain atleast one small and capital letter')
                    return check_passwordformat(input('Re enter password : '))
            else:
                print('password should contain atleast one number')
                return check_passwordformat(input('Re enter password : '))
        else:
            print('password should contain atleast one special character')
            return check_passwordformat(input('Re enter password : '))
    else:
        print('length should be more than 16')
        return check_passwordformat(input('Re enter password : '))

# search and format functions

def forgot_password_option(ui_mailid):
    '''
    it retrives password from the file data('emailid_database.json')(or)
    it updates password in the file data('emailid_database.json')
    :param ui_mailid: validated user input email id string
    :return: the retrived password (or) calls append data to update password
    '''
    with open('emailid_database.json', 'r+') as file:
        file_data = json.load(file)
    print('Enter 1 to retrive password\nEnter 2 to update password')
    options3 = input()
    if options3 == '1':  # retrive
        print(f'registered password : {file_data[ui_mailid]}')
    if options3 == '2':  # create
        update_data(key=ui_mailid)


def password_login(ui_mailid):
    '''
    it takes the user input password from the user and checks the data in the file data (or)
    :param ui_mailid: validated user input mail id string
    :return: if password matchs in the file data print('login successfull')
             if not print('incorrect password') calls the function recursively to re enter the password (or)
             calls the function forgot_password_option(ui_mailid) to either retrive password or update password
    '''
    print('Enter 1 to Enter password\nEnter 2 if forgot password')
    options2 = input()

    with open('emailid_database.json', 'r+') as file:
        file_data = json.load(file)

    if options2 == '1':  # enter password
        ui_password2 = input('Enter password : ')
        if ui_password2 == file_data[ui_mailid]:
            print('login successfull')
        else:
            print('incorrect password')
            password_login(ui_mailid)

    if options2 == '2':  # forgot password
        forgot_password_option(ui_mailid)


def registration():
    '''
    1. it takes input from user and checks the emailid format
    2. checks for existence of id in the database
    3.1.  if exists - 2 options -1. re- enter emailid 2. login
    3.2. if not exists - asks password and checks for the format and creates a dictionary pair of userinput email and password
    4. appends the data to the external json file
    'registration successfull' if all the functions are successfully called and executed
    5. calls the start_program() and present three options
    '''
    # email part
    ui_mailid = check_emailidformat(input('Enter email id : '))
    id_exists = check_id_in_file(ui_mailid)
    if id_exists == True:
        print('Entered emailid already exists\nEnter 1 for re-enter emailid \nEnter 2 for login')
        input1 = input()
        if input1 == '1':
            return registration()
        if input1 == '2':
            return login()
    # password part
    ui_password = check_passwordformat(input('Enter password : '))
    new_data = {ui_mailid: ui_password}
    update_data(new_data=new_data)
    print('registration successfull')
    start_program()


def login():
    '''
    1. it takes input from user and checks the emailid format
    2. checks for existence of id in the database
    3.1. if not exists - 2 options -1. re- enter emailid 2. registration
    3.2. if exists -  asks password and checks in the data base for a match
    3.3.1 if password doesn't match - 2 options - 1.re-enter password 2.forgot password
    3.3.1.1. if forgot password chosen - 2 options - 1. retrive password 2. update password
    3.3.2 if password match - 'login successfull' gets printed
    3.4 calls the start_program() and present three options
    :return:
    '''
    ui_mailid = check_emailidformat(input('Enter email id : '))
    id_exists = check_id_in_file(ui_mailid)
    if id_exists == 'no_data':
        print('zero data exists in the database\nDirecting to registration')
        return registration()
    if id_exists == False:
        print('Entered emailid doesn\'t exists\nEnter 1 for re-enter emailid \nEnter 2 for registration')
        print('')
        input1 = input()
        if input1 == '1':
            return login()
        if input1 == '2':
            return registration()
    password_login(ui_mailid)
    start_program()


def start_program():
    '''
    it selection function to select any of the below options
    1. registration
    2. login
    3. exit the program
    :return: none
    '''
    print('\nEnter 1 for registration\nEnter 2 for login\nEnter 0 to exit the program')
    user_input1 = input()
    if user_input1 == '1':
        registration()
    if user_input1 == '2':
        login()
    if user_input1 == '0':
        exit()

start_program()