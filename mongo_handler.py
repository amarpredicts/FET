from pymongo import MongoClient
import streamlit as st


class MongoDBHandler:
    def __init__(self):
    
        uri = get_uri()
        self.client = MongoClient(uri)
        self.db = self.client.fet_database
        self.coll = self.db.expenses
        # self.coll = self.db.fet_users


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
    
    def insert_salary(self, entry):
        try:
            # Insert the entry into the MongoDB collection
            self.db.salary_expenses.insert_one(entry)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    # Expense Items
            
    def insert_expense(self, entry):
        try:
            # Insert the entry into the MongoDB collection
            self.db.expenses.insert_one(entry)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    def fetch_expenses(self):
        try:
            cursor = self.coll.find()

            # Initialize an empty dictionary to store the entries
            entry_dict = {}

            # Loop through the cursor and populate the dictionary with unique keys
            for idx, doc in enumerate(cursor):

                # Extracting the fields from the document
                country = doc.get('country', '')
                city = doc.get('city', '')
                date = doc.get('date', '')
                activities = doc.get('activities', [])

                # Create a dictionary for the current document
                entry = {
                    "country": country,
                    "city": city,
                    "date": date,
                    "activities": activities
                }

                # Add this entry to the main dictionary with a unique key
                entry_dict[idx] = entry
            return entry_dict
        
        except Exception as e:
            print(f"Error fetching expenses: {e}")
            return []
        

    def fetch_salary_items(self):
            try:
                cursor = self.db.salary_expenses.find()

                # Initialize an empty dictionary to store the entries
                entry_dict = {}

                # Loop through the cursor and populate the dictionary with unique keys
                for idx, doc in enumerate(cursor):

                    # Extracting the fields from the document
                    category = doc.get('category', '')
                    date = doc.get('date', '')
                    amount = doc.get('amount', '')

                    # Create a dictionary for the current document
                    entry = {
                        "category": category,
                        "date": date,
                        "amount": amount,
                    }

                    # Add this entry to the main dictionary with a unique key
                    entry_dict[idx] = entry
                return entry_dict
            
            except Exception as e:
                print(f"Error fetching salary expenses: {e}")
                return []
    

def get_uri():
        MONGO_PWD = st.secrets.MONGO_PWD
        #MONGO_PWD = ""
        if not MONGO_PWD:
            raise ValueError("MONGODB_URI environment variable not set.")
        return f"mongodb+srv://amarpredicts_mongodb:{MONGO_PWD}@amarscluster.fyegt0f.mongodb.net/?retryWrites=true&w=majority"
