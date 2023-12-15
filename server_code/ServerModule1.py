import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
from datetime import datetime, timedelta
import anvil.server
from anvil import tables, app
import time
import random
import uuid
import datetime
# server_module.py

# Function to validate login credentials
@anvil.server.callable
def validate_login(username, password):
    # Query the 'users' table
    user = tables.app_tables.users.get(username=username, password=password)

    if user:
        return user['usertype']
    else:
        return None

@anvil.server.callable
def get_user_for_login(login_input):
  user_by_username = app_tables.users.get(username=login_input)
  if login_input.isdigit():
    phone_number = int(login_input)
    user_by_phone = app_tables.users.get(phone=phone_number)
    return user_by_phone
    # Continue with the rest of your code
  else:
    print("Invalid phone number. Please enter a numeric value.")
  user_by_email = app_tables.users.get(email=login_input)
  if user_by_username:
            return user_by_username
  if user_by_email:
            return user_by_email 
  else:
            return None


@anvil.server.callable
def add_info(email, username, password, pan, address, phone, aadhar):
    user_row = app_tables.users.add_row(
        email=email,
        username=username,
        password=password,
        pan=pan,
        address=address,
        phone=phone,
        aadhar=aadhar,
        usertype='customer',
        confirmed=True,
        limit=str(100000),
        last_login=datetime.datetime.now().date()
    )
    return user_row

@anvil.server.callable
def generate_unique_id(username, phone):
    unique_id = f"{username}-{phone}"

    return unique_id
  

def convert_to_inr(amount, currency):
    conversion_rates = {
        'usd': 75.0,   # Replace with actual rates
        'euro': 85.0,  # Replace with actual rates
        'inr': 1.0,    # 1:1 conversion for INR
        'swiss': 80.0  # Replace with actual rates
        # Add more currencies as needed
    }

    return amount * conversion_rates[currency.lower()]

# Define a function to transfer money to e_wallet
@anvil.server.callable
def transfer_money(username, amount, selected_currency):
    # Get the current user's data from the accounts table
    account_row = app_tables.accounts.get(user=username)

    # Convert the entered amount to INR
    amount_inr = convert_to_inr(float(amount), selected_currency)

    # Update the e_wallet column with the transferred amount
    account_row['e_wallet'] += amount_inr

    # Update the specific currency column with the transferred amount
    currency_column = f'money_{selected_currency.lower()}'
    account_row[currency_column] -= float(amount)

    # Save the changes to the accounts table
    account_row.save()

    # Return a success message or any relevant information
    return f"Transferred {amount} {selected_currency} to e_wallet for {user_id}"


# for deposit
@anvil.server.callable
def get_currency_data(acc):
    currency_table = app_tables.currencies.get(casa= int(acc))
    return currency_table

# fot populating the dropdown section
@anvil.server.callable
def get_user_account_numbers(username):
    # Fetch all matching rows for the specified user
    user_currencies = app_tables.currencies.search(user=username)
    # Extract 'casa' values from all matching rows
    return [str(currency['casa']) for currency in user_currencies]
  
#for the transfer form
@anvil.server.callable
def validate_acc_no_to_display_in_transfer(acc):
  user_validate= app_tables.currencies.get(casa=int(acc))
  return user_validate

#for getting the e_money in accounts
@anvil.server.callable
def get_accounts_emoney(acc):
  user_emoney= app_tables.accounts.get(casa=int(acc))
  return user_emoney

# for keeping the e_wallet same throughout
@anvil.server.callable
def update_all_rows(user,e_money_value):
    # Print statements with proper formatting
    print("hi this is server code")
    print(f"E-money: {e_money_value}")
    matching_rows = app_tables.accounts.search(user=user)
    
    for row in matching_rows:
        row['e_money'] =e_money_value
        row.update()

@anvil.server.callable
def update_rows_emoney_trasaction(wallet, e_money_value):
  matching_rows = app_tables.accounts.search(e_wallet=wallet)
  print("hi we will start deducting")
  for row in matching_rows:
    row['e_money'] = e_money_value
    row.update()

#for getting the e_money in accounts using wallet id
@anvil.server.callable
def get_accounts_emoney_using_wallet_id(wallet):
    print(f"Received wallet ID: {wallet}")

    user_emoney = app_tables.accounts.search(e_wallet=wallet)

    if len(user_emoney) == 1:
        # If only one row is found, return it
        result = user_emoney[0]
        print(f"Found user emoney: {result}")
        return result
    elif len(user_emoney) > 1:
        # If multiple rows are found, handle the first one
        print("Multiple rows found. Handling only the first one.")
        result = user_emoney[0]
        return result
    else:
        # If no rows are found, return None
        print("No matching row found.")
        return None

@anvil.server.callable
def update_daily_limit(name, emoney_value):
    user_row = app_tables.users.get(username=name)  # Use get() instead of search() if username is unique

    if user_row is not None:
        user_row['limit'] = emoney_value
        user_row.update()
        return "Daily limit updated successfully"
    else:
        return "User not found"
  

@anvil.server.callable
def user_detail(name, no):
  user_row = app_tables.users.get(username=name)
  user_row['daily_limit_set']= str(no)
  user_row.update()

@anvil.server.callable
def get_user_info(username):
    user_row = app_tables.users.get(username=username)
    print("get_user_info - user_row:", user_row)  # Add this print statement
    if user_row:
        return {'username': user_row['username'], 'phone': user_row['phone']}
    else:
        return None

# @anvil.server.callable
# def get_accounts_emoney_with_user(name):
#   user_emoney= app_tables.accounts.get(user=name)
#   return user_emoney

@anvil.server.callable
def get_accounts_emoney_with_user(name):
    user_emoney = app_tables.accounts.get(user=name)
    if len(user_emoney) == 1:
        return user_emoney[0]
        print(f"Found user emoney: {result}")
    elif len(user_emoney) > 1:
        # Handle multiple matching rows here, either return a specific one or handle accordingly
        # For example, return the first matching row
        print("Multiple rows found. Handling only the first one.")
        return user_emoney[0]
    else:
        # Handle the case where no rows are found for the given user
        return None
    
    
        
