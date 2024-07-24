from EC_DH import curve, G ,Ka,Kb

# Generate public and private keys for each user
users = [
    {"name": "Amir Mishayev", "id": "318212107", "private_key": Ka, "public_key": curve.scalar_mult(Ka, G)},
    {"name": "Shimron Ifrah", "id": "312423247", "private_key": Kb, "public_key": curve.scalar_mult(Kb, G)},
    {"name": "Anastasya Chesnov", "id": "317450013", "private_key": 25, "public_key": curve.scalar_mult(25, G)},
    {"name": "Alex Baboshin", "id": "310926415", "private_key": 30, "public_key": curve.scalar_mult(30, G)},
]

def find_user_by_name_and_id(name, user_id):
    for user in users:
        if user["name"] == name and user["id"] == user_id:
            return user
    return None
