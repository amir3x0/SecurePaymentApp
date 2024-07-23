from EC_DH import scalar_mult, Point, G, n

# Generate public and private keys for each user
users = [
    {"name": "Amir Mishayev", "id": "318212107", "private_key": 1500, "public_key": scalar_mult(1500, G)},
    {"name": "Shimron Ifrah", "id": "312423247", "private_key": 2000, "public_key": scalar_mult(2000, G)},
    {"name": "Anastasya Chesnov", "id": "317450013", "private_key": 2500, "public_key": scalar_mult(2500, G)},
    {"name": "Alex Baboshin", "id": "310926415", "private_key": 3000, "public_key": scalar_mult(3000, G)},
]

def find_user_by_name_and_id(name, user_id):
    for user in users:
        if user["name"] == name and user["id"] == user_id:
            return user
    return None
