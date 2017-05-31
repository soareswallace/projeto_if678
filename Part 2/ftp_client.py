import socket
import sys

# Read users file
database = dict()
with open("dontOpenPasswordsInside.txt") as db:
    for line in db:
        (usr, psw) = line.split()
        database[usr] = psw

def add_user(store):
    user = raw_input('Create Username: ')
    password = raw_input('Create Password: ')
    if user in database:
        print "That user already exists"
        return False
    else:
        database[user] = password
        return True

opt = 0
while opt != 3:
    print "Select option:"
    print "1. Create user"
    print "2. Upload file"
    print "3. Exit"

    opt = int(raw_input('Enter option: '))
    if(opt == 1):
        add_user(database)
