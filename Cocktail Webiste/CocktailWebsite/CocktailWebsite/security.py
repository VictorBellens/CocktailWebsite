from cryptography.fernet import Fernet

new_password = {}

bucket0 = []
bucket1 = []
bucket2 = []
bucket3 = []
bucket4 = []
bucket5 = []
bucket6 = []
bucket7 = []
bucket8 = []
bucket9 = []
bucket10 = []
bucket11 = []
bucket12 = []
bucket13 = []
bucket14 = []
bucket15 = []
bucket16 = []


def find_bucket_value(username, password): # locates the bucket in which the password lies
    bucket_value = 32
    username_value = 0
    password_value = 0

    for letter in username: # changing letters to ASCII values for calculations
        val = ord(letter)
        username_value += val

    for letter in password:
        val = ord(letter)
        password_value += val

    final_value = (username_value * password_value) % bucket_value # finds a bucket value between 1 and 32 using the username and unencrypted password
    return final_value


def enc_message(message):
    key_hash_pair = []
    key = Fernet.generate_key()
    fernet = Fernet(key)

    encMessage = fernet.encrypt(message.encode()) # encrypted password using Fernet module

    key_hash_pair.append(key) # the key used to decrypt the encrypted password
    key_hash_pair.append(encMessage)
    return key_hash_pair


# bucket_value = find_bucket_value(username, password)
# new_password[username] = enc_message(password)

# print(bucket_value)
# print(new_password)


def dec_message(message, name):
    key = message[name][0]
    password = message[name][1]

    fernet = Fernet(key)
    decMessage = fernet.decrypt(password).decode() # decodes the password when given the correct key

    return decMessage


# print(new_password)
# print(dec_message(new_password, username))