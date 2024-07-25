from EC_DH import curve, G ,private_keys,public_keys
from schnorr import schnorr_public_keys 

# Generate public and private keys for each user
users = [
    {"name": "Amir Mishayev", "id": "318212107", "private_key": private_keys, "public_key": public_keys,"schnor_public_key": schnorr_public_keys},
    {"name": "Shimron Ifrah", "id": "312423247", "private_key": private_keys, "public_key": public_keys, "schnor_public_key": schnorr_public_keys},
    {"name": "Anastasya Chesnov", "id": "317450013", "private_key": private_keys, "public_key": public_keys, "schnor_public_key": schnorr_public_keys},
    {"name": "Alex Baboshin", "id": "310926415", "private_key": private_keys, "public_key": public_keys, "schnor_public_key": schnorr_public_keys},
]

def find_user_by_name_and_id(name, user_id):
    for user in users:
        if user["name"] == name and user["id"] == user_id:
            return user
    return None
