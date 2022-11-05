from cryptography.fernet import Fernet
 
# key = Fernet.generate_key() 

def encrypt(key, string):
    fernet = Fernet(key)
    return fernet.encrypt(string.encode())

def decrypt(key, string):
    fernet = Fernet(key)
    return fernet.decrypt(string).decode()

# reference: https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/