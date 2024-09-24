import os
import shutil
import getpass
from cryptography.fernet import Fernet

# Generate a key and save it in the .key directory
def generate_key():
    if not os.path.exists(".key"):
        os.mkdir(".key")
        os.system("attrib +h .key")  # Make the key file hidden (Windows)
        key = Fernet.generate_key()
        with open(".key/key.key", "wb") as key_file:
            key_file.write(key)
        print("Encryption key generated and saved.")
    else:
        print("Key already exists. Not generating a new one.")

# Load the encryption key from the .key directory
def load_key():
    try:
        return open(".key/key.key", "rb").read()
    except FileNotFoundError:
        raise Exception("Encryption key not found. Ensure the key exists in the '.key' directory.")

# Encrypt a single file
def encrypt_file(filename, key):
    try:
        f = Fernet(key)
        with open(filename, "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(filename, "wb") as file:
            file.write(encrypted_data)
        print(f"Encrypted: {filename}")
    except Exception as e:
        print(f"Failed to encrypt {filename}: {e}")

# Decrypt a single file
def decrypt_file(filename, key):
    try:
        f = Fernet(key)
        with open(filename, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(filename, "wb") as file:
            file.write(decrypted_data)
        print(f"Decrypted: {filename}")
        return True
    except Exception as e:
        print(f"Error decrypting file {filename}: {e}")
        return False

# Save folder structure to a file
def save_structure(folder):
    structure = []
    for root, dirs, files in os.walk(folder):
        for dir_name in dirs:
            relative_path = os.path.relpath(os.path.join(root, dir_name), folder)
            structure.append(relative_path)
    return "\n".join(structure)

# Load folder structure from an encrypted file
def load_structure(filename, key):
    try:
        with open(filename, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = Fernet(key).decrypt(encrypted_data).decode()
        return decrypted_data.splitlines()
    except Exception as e:
        raise Exception(f"Failed to load folder structure: {e}")


# Combine multiple files into a single binary file
def folder_to_file(folder):
    structure = save_structure(folder)
    with open(f"{folder}.bin", "wb") as new_file:
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                if ".key" in file_path:
                    continue  # Skip the .key directory
                
                relative_path = os.path.relpath(file_path, folder)
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    new_file.write(len(relative_path).to_bytes(1, 'big') + relative_path.encode() + len(file_data).to_bytes(4, 'big') + file_data)
    
    shutil.rmtree(folder, ignore_errors=True)
    shutil.move(f"{folder}.bin", ".key")

    # Save the folder structure in the .key directory in encrypted form
    key = load_key()
    f = Fernet(key)
    encrypted_structure = f.encrypt(structure.encode())
    with open(".key/structure.enc", "wb") as structure_file:
        structure_file.write(encrypted_structure)

# Split a single binary file back into multiple files
def file_to_folder(file):
    folder_name = file.split(".")[0]
    os.mkdir(folder_name)
    
    with open(file, "rb") as f:
        file_data = f.read()
    
    index = 0
    while index < len(file_data):
        length = int.from_bytes(file_data[index:index+1], 'big')
        index += 1
        file_name = file_data[index:index+length].decode()
        index += length
        data_length = int.from_bytes(file_data[index:index+4], 'big')
        index += 4
        file_content = file_data[index:index+data_length]
        index += data_length
        
        full_file_path = os.path.join(folder_name, file_name)
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)  # Create necessary subfolders
        with open(full_file_path, "wb") as new_file:
            new_file.write(file_content)

    os.remove(file)

# Encrypt all files in a folder and store them in a new folder called "Locked"
def lock_files(folder, password):
    current_dir = os.getcwd()
    os.chdir(folder)
    
    generate_key()
    key = load_key()
    
    if not os.path.exists("Locked"):
        os.mkdir("Locked")
    
    for root, dirs, files in os.walk(folder):
        if ".key" in dirs:
            dirs.remove(".key")  # Skip the .key directory
        if "Locked" in dirs:
            dirs.remove("Locked")
        
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, folder)
            target_path = os.path.join("Locked", relative_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.move(source_path, target_path)
    
    for root, _, files in os.walk("Locked"):
        for file in files:
            encrypt_file(os.path.join(root, file), key)
    
    with open("Locked/password.txt", "wb") as f:
        f.write(password.encode())
    encrypt_file("Locked/password.txt", key)

    shutil.move("Locked/password.txt", ".key")
    folder_to_file("Locked")
    
    with open("README.md", "w", encoding='utf-8') as f:
        f.write(
            "# Loa Notice\n\n"
            "These files are locked. To unlock them, use the `loa.py` script.\n"
            "Do not delete the `.key` directory. Do not delete this file.\n"
            "Kindly contact the owner of the files for the password.\n"
            "Thank you.\n\n"

            "---\n\n"

            "_God Hates Me_ :( And I hate myself too.\n"
            "I'm a failure. I'm a loser. I'm a nobody and I'm nothing to anyone.\n"
            "I'm a waste of space and a waste of time.\n"
            "I'm a waste of life. I'm a waste of everything.\n"
            "I'm a waste of oxygen. I'm a waste of resources.\n"
            "I'm a waste of money. I'm a waste of effort.\n\n"

            "---\n\n"

            "<div  align=\"center\">\n"
            "✨ loa, 2024, All Rights Reserved.\n"
            "</div>\n"  
        )
    
    if not os.path.exists(".key/key.key"):
        with open(".key/key.key", "wb") as key_file:
            key_file.write(key)
    
    os.chdir(current_dir)

# Decrypt all files from the "Locked" folder
def unlock_files(folder, password):
    current_dir = os.getcwd()
    os.chdir(folder)
    
    key = load_key()
    shutil.move(".key/Locked.bin", ".")
    file_to_folder("Locked.bin")

    structure_file_path = ".key/structure.enc"
    folder_structure = load_structure(structure_file_path, key)

    for subfolder in folder_structure:
        os.makedirs(os.path.join(folder, subfolder), exist_ok=True)

    for root, _, files in os.walk("Locked"):
        for file in files:
            decrypt_file(os.path.join(root, file), key)
    
    with open(".key/password.txt", "rb") as password_file:
        encrypted_password = password_file.read()
    
    decrypted_password = Fernet(key).decrypt(encrypted_password).decode()
    
    if password == decrypted_password:
        for root, _, files in os.walk("Locked"):
            for file in files:
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, "Locked")
                target_path = os.path.join(folder, relative_path)
                shutil.move(source_path, target_path)
        
        shutil.rmtree("Locked")
    else:
        print("Incorrect password. Files are still locked.")
    
    shutil.rmtree(".key")
    os.remove("README.md")
    os.chdir(current_dir)

def run():
    if not os.path.exists(f"{folder}/README.md"):
        password = getpass.getpass("Enter a password to lock the files: ")
        lock_files(folder, password)
    else:
        print("README.md already exists. Skipping lock process.")
        unlock_password = getpass.getpass("Enter the password to unlock the files: ")
        unlock_files(folder, unlock_password)

# Example usage
folder = "./luames"  # Replace with the folder to lock/unlock
run()

