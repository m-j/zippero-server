import bcrypt
import sys
import base64


def hash_password(password: str):
    password_bytes = bytes(password, 'utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    base_64_hashed = base64.b64encode(hashed).decode('utf-8')
    return base_64_hashed


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python hash-password.py [your_password]')
    else:
        print(hash_password(sys.argv[1]))