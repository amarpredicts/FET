from deta import Deta

DETA_KEY = "hv4CPkKC_eEXFPQrzx2V1mdZDPBx2yLPHXRhEFi4c"

# Init deta account

deta = Deta(DETA_KEY)

# Create/connect a database

db = deta.Base("fet_users_db")

def insert_user(username, password):
    """Returns the user on a successful user creation, otherwise throws an error."""
    db.put({"username": username,
            "password": password
            })
    
insert_user("pparker", "abc123")