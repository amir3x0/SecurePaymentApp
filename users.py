# users.py

from EC_DH import scalar_mult, Point, G

# Generate public and private keys for each user
users = [
    {"name": "Amir Mishayev", "id": "318212107", "private_key": 5, "public_key": scalar_mult(5, G)},
    {"name": "Shimron Ifrah", "id": "312423247", "private_key": 7, "public_key": scalar_mult(7, G)},
    {"name": "Anastasya Chesnov", "id": "317450013", "private_key": 11, "public_key": scalar_mult(11, G)},
    {"name": "Alex Baboshin", "id": "310926415", "private_key": 13, "public_key": scalar_mult(13, G)},
]

def find_user_by_name_and_id(name, user_id):
    for user in users:
        if user["name"] == name and user["id"] == user_id:
            return user
    return None
