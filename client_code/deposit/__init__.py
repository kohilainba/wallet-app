from ._anvil_designer import depositTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime


class deposit(depositTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.label_1.text = f"Welcome to Green Gate Financial, {user['username']}"
        print(f"User parameter in deposit form: {user}")
        self.user = user
        self.init_components(**properties)

  
    def button_1_click(self, **event_args):
        current_datetime = datetime.now()

        if self.user is not None:
            wallet3 = anvil.server.call('generate_unique_id', self.user['username'], self.user['phone'])

            if wallet3 is None:
                self.label_2.text = "Error: Wallet is empty"
                return

            money3_numeric = ''.join(filter(str.isdigit, str(self.text_box_3.text)))
            money_value = float(money3_numeric) if money3_numeric else 0.0

            selected_symbol = self.drop_down_1.selected_value

            entered_account_number = self.text_box_2.text

            user_currencies = anvil.server.call('get_currency_data', entered_account_number)

            if len(str(entered_account_number)) < 10 or not str(entered_account_number).isdigit():
                self.label_2.text = "Error: Invalid account number. Please enter at least 10 digits."
                return

            if user_currencies is not None:
                user_currency = user_currencies

                if selected_symbol == '€':
                    user_currency['money_euro'] = str((float(user_currency['money_euro'] or 0)) + money_value)
                elif selected_symbol == '$':
                    user_currency['money_usd'] = str((float(user_currency['money_usd'] or 0)) + money_value)
                elif selected_symbol == '₣':
                    user_currency['money_swis'] = str((float(user_currency['money_swis'] or 0)) + money_value)
                elif selected_symbol == '₹':
                    user_currency['money_inr'] = str((float(user_currency['money_inr'] or 0)) + money_value)
                else:
                    self.label_2.text = "Error: Invalid currency symbol selected."
                    return

                user_currency.update()

                # Convert deposited amount to INR
                inr_value = money_value
                if selected_symbol != '₹':
                    # Define exchange rates (you need to fetch these dynamically from an API or another source)
                    exchange_rates = {'$': 74.5, '€': 88.2, '₣': 80.0}  # Example rates
                    inr_value = money_value * exchange_rates[selected_symbol]

                # Update the user's limit in INR
                remaining_limit = int(self.user['limit'] or 0) - inr_value
                if remaining_limit < 0:
                    alert("Limit exceeded. Cannot deposit more than the limit.")
                    return  # Return to prevent storing negative value in 'limit' column and further execution

                self.user['limit'] = remaining_limit
                self.user.update()

                new_transaction = app_tables.transactions.add_row(
                    user=self.user['username'],
                    casa=int(entered_account_number),
                    e_wallet=wallet3,
                    money=f"{selected_symbol}-{money_value}",
                    date=current_datetime,
                    transaction_type="Deposit"
                )

                self.label_2.text = "Money added successfully to the account. Remaining limit: {}".format(remaining_limit)
            else:
                self.label_2.text = "Error: No matching accounts found for the user or invalid account number."
        else:
            self.label_2.text = "Error: User information is not available"

    def link_click(self, **event_args):
        open_form('customer', user=self.user)

    def link_9_click(self, **event_args):
        open_form('transfer', user=self.user)

    def link_10_click(self, **event_args):
        open_form('withdraw', user=self.user)
