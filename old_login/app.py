from mongo_handler import MongoDBHandler
from old_login.landing_page import open_landing_page
import streamlit_authenticator as stauth
import streamlit as st


def register(mongo_handler):
    with st.form("register_form"):
        st.subheader("Register")
        new_username = st.text_input("Username")
        new_name = st.text_input("Full Name")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.form_submit_button("Register") is True:
            print("The register Button was pressed")
            # Validate passwords match
            if new_password == confirm_password and new_password is not "":
                # Register user
                hashed_pw = stauth.Hasher([new_password]).generate()
                result = mongo_handler.register_user(new_username, new_name, hashed_pw[0])

                if result:
                    st.success("Registration successful!")
                    #TODO: Redirect to the main content or show a success message
                else:
                    st.error("Registration failed. Please try again.")
            else:
                st.warning("Passwords do not match or empty. Please try again.")

def login(auth):
    name , authentication_status, username = auth.login('Login', 'main')

def expand_options(mongo_handler, auth):
    with st.expander("Login here"):
        login(auth)
    if not st.session_state["authentication_status"] is True:
        with st.expander("Register here"):
            register(mongo_handler)

#@st.cache_data
def get_credentials_dict(_mongo_handler):
    return _mongo_handler.get_all_users()


def main():

    print("Main starts")

    st.set_page_config(page_title="FET", page_icon=":airplane:")
    st.title(":airplane: Flight Expense Tracker")

    # Create MongoDBHandler instance using information from environment variables
    mongo_handler = MongoDBHandler()
    credentials_dict = get_credentials_dict(mongo_handler)

    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
        
    auth = stauth.Authenticate(credentials_dict, "Flight Expense Tracker", "SecretKey", cookie_expiry_days=7)
    
    if st.session_state["authentication_status"] == None:
        expand_options(mongo_handler, auth)

    if st.session_state["authentication_status"] == False:
        st.toast(":red[Username/password is incorrect]", icon= "🚨")

    if st.session_state["authentication_status"] == True:
        open_landing_page()
        auth.logout("Logout", "sidebar", "unique_logout_button")

    # Close the MongoDB connection
    mongo_handler.close_connection()


if __name__ == "__main__":
    main()

