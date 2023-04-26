# Import streamlit and other modules
import streamlit as st
import pandas as pd
import hashlib

# Define a filename to store the user credentials
filename = 'credentials.csv'

# Load the dataframe from the file if it exists, or create a new one
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    df = pd.DataFrame({
        'username': ['admin'],
        'password': ['5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8', # hash of 'password'
                     'e38ad214943daad1d64c102faec29de4afe9da3d', # hash of 'streamlit'
                     '5e52fee47e6f95708eab44de4c0f3dab9d21b9db'] # hash of 'python'
    })

# Define a function to hash passwords
def hash_password(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()

# Define a function to check if the username and password are valid
def check_credentials(username, password):
    password_hash = hash_password(password)
    return (username in df['username'].values) and (password_hash == df[df['username'] == username]['password'].iloc[0])

# Define a function to register a new account
def register_account(username, password):
    password_hash = hash_password(password)
    if username in df['username'].values:
        return False
    # Append the new credentials to the dataframe
    df.loc[len(df)] = [username, password_hash]
    # Save the dataframe to the file
    df.to_csv(filename, index=False)
    return True

# Create a title and a sidebar
st.title('Login System')
sidebar = st.sidebar

# Ask the user to choose between login or register in the sidebar
mode = sidebar.radio('Choose mode', ['Login', 'Register'])

# If the user chooses login, ask them to enter username and password in the sidebar
if mode == 'Login':
    username = sidebar.text_input('Username')
    password = sidebar.text_input('Password', type='password')

    # If the user clicks the login button, check the credentials and display a message
    if sidebar.button('Login'):
        if check_credentials(username, password):
            st.success(f'Logged in as {username}')
            # You can add your app logic here

            # Add a button to log out
            if st.button('Log out'):
                st.info('Logged out successfully.')
                # Clear the username and password inputs
                sidebar.empty()
                # Reload the page
                st.experimental_rerun()
        else:
            st.error('Invalid username or password')

elif mode == 'Register':
    new_username = sidebar.text_input('New username')
    new_password = sidebar.text_input('New password', type='password')

    # If the user clicks the register button, register a new account and display a message
    if sidebar.button('Register'):
        if register_account(new_username, new_password):
            st.success('Registered successfully. You can now login with your new credentials.')
        else:
            st.error('Username already taken. Please choose a different one.')
