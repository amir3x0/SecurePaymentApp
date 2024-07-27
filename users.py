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
    """
    Find a user by their name and ID.

    Args:
        name (str): The name of the user to search for.
        user_id (int): The ID of the user to search for.

    Returns:
        dict or None: The user dictionary if found, None otherwise.
    """
    for user in users:
        if user["name"] == name and user["id"] == user_id:
            return user
    return None
