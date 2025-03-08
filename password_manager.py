from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from hashlib import sha256
file_path = ".\\password.txt"

try:
    with open(file_path, 'r') as file:
        print("Password file exists.")
        data = file.readlines()
except:
    print("Password file does not exist.")
    try:
        with open(".\\backup.txt", 'r') as file:
            print("Backup file exists.")
            data = file.readlines()
            with open(".\\password.txt", 'w') as file:
                file.writelines(data)
    except:
        print("Backup file does not exist.")
        with open('.\\backup.txt', 'w') as file:
            file.writelines([])
        with open('.\\password.txt', 'w') as file:
            file.writelines([])
try:
    with open('.\\login.txt', 'r') as file:
        print("Login file exists.")
        data = file.readlines()
    if data==[]:
        print("Login file is empty.")
        with open('.\\password.txt', 'w') as file:
            file.writelines([])
except:
    print("Login file does not exist. Creating new login file.")
    data=[]
    with open('.\\login.txt', 'w') as file:
        file.writelines(data)
        with open('.\\password.txt', 'w') as file:
            file.writelines([])
        

def read_key():
    with open('.\\login.txt', 'r') as file:
        data = file.readlines()
    return data[1]

def encrypt_message(message):
    key=read_key()
    key=bytes.fromhex(key)
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
        iv = cipher.iv
        return ciphertext, iv
    except (ValueError, KeyError) as e:
        print(f"An error occurred: {e}")
        return None, None
def decrypt_message_og(site):
    key=read_key()
    key=bytes.fromhex(key)
    try:
        ciphertext,iv=must_for_decrypt_og(site)
        cipher = AES.new(key, AES.MODE_CBC,iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext_bytes = unpad(padded_plaintext, AES.block_size)
        plaintext = plaintext_bytes.decode("utf-8")
        return plaintext
    except (ValueError, KeyError) as e:
        print(f"An error occurred: {e}")
        return "Wrong key."

def must_for_decrypt_og(site):
    with open(file_path, 'r') as file:
        data = file.readlines()
    for line in data:
        words=line.split()
        if(site==bytes.fromhex(words[0]).decode('utf-8')):
            ciphertext=bytes.fromhex(words[1])
            iv=bytes.fromhex(words[2])
            return ciphertext,iv
# Get the key string from the user
def check_key(user_input):
    key_string=user_input
    # Hash the key string to create a 256-bit key
    key = SHA256.new(key_string.encode()).digest()
    with open(".\\login.txt", 'r') as file:
        data = file.readlines()
    #print(len(data),data)

    hash_string=data[1]
    if(hash_string==key.hex()):
        return True
    return False

def get_key(user_input):
    key_string=user_input
    # Hash the key string to create a 256-bit key
    key = SHA256.new(key_string.encode()).digest()
    return key

def get_sites():
    with open(file_path, 'r') as file:
        data = file.readlines()
    sites=[]
    for line in data:
        words=line.split()
        sites.append(bytes.fromhex(words[0]).decode('utf-8'))
    return sites

def new_key(user_input):
    key_string=user_input
    # Hash the key string to create a 256-bit key
    key = SHA256.new(key_string.encode()).digest()
    data=['logged_in'+'\n',key.hex()]
    with open('.\\login.txt', 'w') as file:
        file.writelines(data)

def backup_passwords():
    with open(file_path, 'r') as file:
        data = file.readlines()
    backup=[]
    for line in data:
        words=line.split()
        site=words[0]
        ciphertext=words[1]
        iv=words[2]
        backup.append(site+" "+ciphertext+" "+iv+"\n")
    with open(".\\backup.txt", 'w') as file:
        file.writelines(backup)

def choice_1(site,password):
    ciphertext,iv=encrypt_message(password)
    site=site.encode('utf-8')
    with open(file_path, 'r') as file:
        data = file.readlines()
    if(data==[]):
        data.append(site.hex()+" "+ciphertext.hex()+" "+iv.hex()+"\n")
    else:
        check=False
        for line in data:
            if(site.hex() in line):
                check=True
                break
        if(check):
            #print("Site already exists. Overwrite? (y/n)")
            data_no = [line for line in data]
            data_yes = [line for line in data if site.hex() not in line]
            data_yes.append(site.hex()+" "+ciphertext.hex()+" "+iv.hex()+"\n")
            return data_no,data_yes
        else:
            data.append(site.hex()+" "+ciphertext.hex()+" "+iv.hex()+"\n")
    with open(file_path, 'w') as file:
        file.writelines(data)
    return None,None

def encrypt_with_new_key(new_key):
    with open(file_path, 'r') as file:
        data = file.readlines()
    new_data=[]
    new_key=SHA256.new(new_key.encode()).digest()
    for line in data:
        words=line.split()
        site=bytes.fromhex(words[0]).decode('utf-8')
        password=decrypt_message_og(site)
        pair=(site,password)
        new_data.append(pair)
    with open(".\\login.txt", 'w') as file:
        file.writelines("logged_in\n"+new_key.hex())
    new_passwords=[]
    for pairs in new_data:
        site=pairs[0]
        site=site.encode('utf-8')
        password=pairs[1]
        ciphertext,iv=encrypt_message(password)
        new_passwords.append(site.hex()+" "+ciphertext.hex()+" "+iv.hex()+"\n")
    with open(file_path, 'w') as file:
        file.writelines(new_passwords)

def main_function(key):
    print("1. Encrypt")
    print("2. Decrypt")
    choice=input()
    while(choice!='0'):
        with open(file_path, 'r') as file:
            data = file.readlines()
        if(choice=='1'):
            print("Enter site: ")
            site=input()
            password=input()
            ciphertext,iv=encrypt_message(password,key)
            if(data==[]):
                data.append(site.hex()+" "+ciphertext.hex()+" "+iv.hex()+"\n")
            else:
                check=False
                for line in data:
                    if(site.hex() in line):
                        check=True
                if(check):
                        print("Site already exists. Overwrite? (y/n)")
                        choice=input()
                        if(choice=='n'):
                            data = [line for line in data]
                        else:
                            data = [line for line in data if site.hex() not in line]
                            data.append(site.hex()+" "+ciphertext.hex()+" "+iv.hex()+"\n")
                else:
                    data.append(site.hex()+" "+ciphertext.hex()+" "+iv.hex()+"\n")        
            with open(file_path, 'w') as file:
                file.writelines(data)
        elif(choice=='2'):
            print("Enter site:")
            site=input()
            for line in data:
                words=line.split()
                if(site.hex()==words[0]):
                    ciphertext=bytes.fromhex(words[1])
                    iv=bytes.fromhex(words[2])
                    break
            plaintext=decrypt_message_og(key,site)
            print(plaintext)
        print("1. Encrypt")
        print("2. Decrypt")
        choice=input()
    
