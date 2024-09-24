# Loa File Locking Script

## Introduction

`loa.py` is a Python script designed to securely lock and unlock files within a specified folder using password-based encryption. It leverages the `cryptography` library to encrypt files, ensuring that sensitive data remains confidential. This script is particularly useful for users who need to protect files temporarily or prevent unauthorized access.

## Features

- **Password Protection**: Encrypt and decrypt files using a user-provided password.
- **Hidden Encryption Key**: Stores the encryption key in a hidden directory to enhance security.
- **Folder Structure Preservation**: Maintains the original folder structure during encryption and decryption.
- **Single Binary File Storage**: Combines all encrypted files into a single binary file for efficient storage.
- **Automated Process**: Automatically detects whether to lock or unlock files based on the presence of specific files.

## Prerequisites

- **Python 3.x**: Ensure Python 3 is installed on your system.
- **Cryptography Library**: Install the required library by running:

  ```bash
  pip install cryptography
  ```

## Folder and File Naming Conventions

- **`loa.py`**: The main script responsible for encrypting and decrypting files. Its name is kept simple and self-explanatory, indicating its purpose (lock/unlock files).
- **`.key/` Directory**: This hidden directory contains the encryption key (`key.key`), encrypted password (`password.txt`), and folder structure (`structure.enc`). It is vital for the decryption process.

  - **`.key/key.key`**: Stores the symmetric encryption key used for encrypting and decrypting files.
  - **`.key/password.txt`**: Contains the encrypted password provided by the user.
  - **`.key/structure.enc`**: Stores the encrypted folder structure, ensuring files are restored to their original state during decryption.
- **`Locked/` Folder**: A temporary folder created during the encryption process that holds the files before they are combined into a binary file.
- **`Locked.bin`**: The binary file that contains all encrypted files from the folder. It is stored inside the `.key` directory after encryption.
- **`README.md`**: This file is generated during the locking process, providing instructions and notices to users. It is used as an indicator for the lock state and contains specific guidelines.

### Naming Logic:

- Names such as `.key`, `Locked`, and `Locked.bin` follow a descriptive convention, indicating their roles in the locking/unlocking process. The use of a hidden `.key` folder emphasizes its critical and confidential nature, reducing the risk of accidental deletion.

## Usage

1. **Locking Files**

   - Open a terminal or command prompt in the directory containing `loa.py`.
   - Run the script:

     ```bash
     python loa.py
     ```
   - Since the files are not yet locked, the script will prompt:

     ```
     Enter a password to lock the files:
     ```
   - Enter a strong password and press Enter. The script will:

     - Generate an encryption key and store it in a hidden `.key` directory.
     - Encrypt all files within the `luames` folder.
     - Combine encrypted files into a `Locked.bin` file and store it in the `.key` directory.
     - Save the encrypted folder structure.
     - Create a `README.md` file with instructions.
2. **Unlocking Files**

   - Run the script again:

     ```bash
     python loa.py
     ```
   - The script detects that the files are locked and prompts:

     ```
     Enter the password to unlock the files:
     ```
   - Enter the password used during the locking process. The script will:

     - Decrypt the `Locked.bin` file and reconstruct the original folder and files.
     - Verify the password. If correct, it restores the files; if not, it notifies you of the incorrect password.
     - Clean up by deleting the `.key` directory and `README.md` file.

## Key Functions

### `generate_key()`

- This function generates a new encryption key using the `Fernet` symmetric encryption algorithm. The key is stored in the hidden `.key` directory. If the directory already exists, the function avoids generating a new key.

### `load_key()`

- This function loads the encryption key from the `.key/key.key` file, essential for encrypting or decrypting files. If the key is missing, it raises an error.

### `encrypt_file(filename, key)`

- Encrypts the contents of the specified file using the provided key. The encrypted data overwrites the original file.

### `decrypt_file(filename, key)`

- Decrypts the specified encrypted file using the key. The decrypted data overwrites the encrypted file. If the decryption fails, an error message is returned.

### `folder_to_file(folder)`

- Combines all the files in a folder into a single binary file (`Locked.bin`), preserving the folder structure. The encrypted folder structure is stored in `.key/structure.enc`.

### `file_to_folder(file)`

- Reverses the `folder_to_file()` function, extracting individual files from the binary file and recreating the original folder structure.

### `lock_files(folder, password)`

- Encrypts all files in the given folder, moves them into a "Locked" directory, and stores the encrypted binary file in `.key`.

### `unlock_files(folder, password)`

- Decrypts and restores the original files from the "Locked" binary file, given the correct password.

## Notes

- **Do Not Delete `.key` Directory**: The `.key` directory contains the encryption key, password, and folder structure needed to unlock your files. Deleting this directory will result in irreversible data loss.
- **Secure Your Password**: Losing the password used during the locking process will prevent you from unlocking the files. The password is stored in encrypted form inside `.key/password.txt`, and the correct password is required for decryption.
- **Do Not Modify `README.md`**: This file serves as an indicator of whether the files are locked or unlocked. Altering or deleting this file may interfere with the script’s functionality.

## Security Considerations

- **Hidden Files**: The script uses hidden directories and files (`.key`) to store sensitive information such as encryption keys and passwords.
- **Encryption**: Files are encrypted using `Fernet`, a symmetric encryption method from the `cryptography` library, which is widely recognized for secure encryption.

## License and Attribution

- **Author**: [Prabin Panta](https://github.com/prabinpanta0)
- **Year**: 2024
- **All Rights Reserved**
- **LICENSE** : [MIT](LICENSE)

## Contact
For more information, visit:

**Instagram:** [prabinpanta0](https://www.instagram.com/prabinpanta0/)  
**Email:** [pantaprabin30@gmail.com](mailto:pantaprabin30@gmail.com)
**Instant Message:** [Instant Message](https://prabinpanta0.github.io/glowing-enigma/)

## Disclaimer

The script is provided "as is" without warranty of any kind. The author is not responsible for any data loss or other damages arising from the use of this script. Use it at your own risk.

---

**Note**: This script includes a `README.md` file generated during the locking process containing specific notices and messages. Be sure to read it carefully when your files are locked.
