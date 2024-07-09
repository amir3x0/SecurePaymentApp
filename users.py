
users = [
    {"name": "Amir Mishayev", "id": "318212107"},
    {"name": "Shimron Ifrah", "id": "312423247"},
    {"name": "Anastasya Chesnov", "id": "317450013"},
    {"name": "Alex Baboshin", "id": "310926415"}
]

def find_user_by_name_and_id(name, user_id):
    for user in users:
        if user["name"] == name and user["id"] == user_id:
            return user
    return None
