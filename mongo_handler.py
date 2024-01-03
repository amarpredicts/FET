from pymongo import MongoClient
import streamlit as st


class MongoDBHandler:
    def __init__(self):
    
        uri = get_uri()
        self.client = MongoClient(uri)
        self.db = self.client.fet_database
        self.coll = self.db.fet_users


    def close_connection(self):
        """Close the connection to MongoDB."""
        self.client.close()


    def register_user(self, username, name, password):
        """Create a new user entry in the database."""
        # Implement user registration logic here
        # For simplicity, I'm using the insert_user method
        return self.coll.insert_one({"user": username, "name": name, "password": password})
    

    def find_user(self, username, password):
        """Find the user in the database."""
        # Implement user authentication logic here
        # For simplicity, I'm using a basic check for username and password match
        return self.coll.find_one({"user": username, "password": password})


    def get_all_users(self):
        cursor = self.coll.find()
        # Create an empty dictionary to store user credentials
        credentials_dict = {'usernames': {}}

        # Loop through the cursor and populate the dictionary
        for doc in cursor:
            user = doc['user'].lower()
            password = doc['password']
            names = doc['name']
            credentials_dict['usernames'][user] = {'password': password, 'name': names}
        
        return credentials_dict
    

def get_uri():
        MONGO_PWD = st.secrets.MONGO_PWD
        if not MONGO_PWD:
            raise ValueError("MONGODB_URI environment variable not set.")
        return f"mongodb+srv://amarpredicts_mongodb:{MONGO_PWD}@amarscluster.fyegt0f.mongodb.net/?retryWrites=true&w=majority"
