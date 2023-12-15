from ._anvil_designer import e_wallet_to_e_walletTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class e_wallet_to_e_wallet(e_wallet_to_e_walletTemplate):
  
    def __init__(self, user=None, **properties):
        self.user = user
        self.init_components(**properties)
        self.label_1.text = f"Welcome to Green Gate Financial, {user['username']}"


    def button_1_click(self, **event_args):
        current_datetime = datetime.now()
        depoitor = self.text_box_1.text
        wallet_id = self.text_box_2.text
        transfer_amount = self.text_box_3.text
        
        depositor_wallet_id= anvil.server.call('generate_unique_id', self.user['username'], self.user['phone'])
        #getting the depositor's details
        fore_money_depositor = anvil.server.call('get_accounts_emoney_using_wallet_id', depositor_wallet_id)
        #getting the reciever's details
        fore_money_sent = anvil.server.call('get_accounts_emoney_using_wallet_id',wallet_id)
      
        if (transfer_amount < 5) or (transfer_amount > 50000):
           self.label_4.text = "Transfer amount should be between 5 and 50000 for a transfer Funds." 
        else:
           if float(fore_money_depositor['e_money']) < transfer_amount:
             self.label_4.text = "Insufficient Funds in E-Wallet."
           else: 
             #calculating the money to be added in the recieve's end
             transfer_fianl_sent_amount= float(fore_money_sent['e_money']) + transfer_amount
             #calculating the money to be deducted in the depositor's end
             transfer_amount_final = float(fore_money_depositor['e_money'])-transfer_amount
             #setting the value
             anvil.server.call('update_rows_emoney_trasaction',depositor_wallet_id, str(transfer_amount_final))
             anvil.server.call('update_rows_emoney_trasaction',wallet_id, str(transfer_fianl_sent_amount))
             #Updating the daily limit
             answer = float(self.user['limit'])- transfer_amount
             anvil.server.call('update_daily_limit', self.user['username'], str(answer))
             self.label_4.text = "Money transferred successfully"

             app_tables.transactions.add_row(
                 user=self.user['username'],
                 e_wallet=f"{depositor_wallet_id} to {wallet_id}",
                 money=f"Transfer-{transfer_amount}",
                 date=current_datetime,
                 transaction_type="E-wallet to E-wallet"
               )
        user =app_tables.users.get(top_up=True)
        if user is not None and user['top_up']:
          for_emoney = anvil.server.call('get_accounts_emoney_with_user',self.user['username'])
          money_in_emoney= for_emoney['e_money']
          threshold =2000
          if float(money_in_emoney)< threshold:
            final= str(float(money_in_emoney) + 5000)
            if self.deduct_currencies(final):
              anvil.server.call('update_all_rows',self.user['username'], final)
              self.button_1.visible = False
              self.button_2.visible = True
          else:
            return f"E-wallet balance ({money_in_emoney}) is above the threshold. No top-up needed."
            
          

    def deduct_currencies(self, amount):
      acc= self.dropdown_account_numbers.selected_value
      currencies_table = app_tables.currencies.get(casa=int(acc))
      conversion_usd = float(currencies_table['money_usd'])*80
      conversion_euro = float(currencies_table['money_euro'])*85
      conversion_swis = float(currencies_table['money_swis']) * 90
      conversion_inr = float(currencies_table['money_inr']) * 1 
      if conversion_usd > 5000:
        currencies_table['money_usd'] = str((conversion_usd- 5000)/80)
        currencies_table.update()
      elif conversion_euro  > 5000:
        currencies_table['money_euro'] = str((conversion_euro- 5000)/85)
        currencies_table.update()
      elif conversion_swis > 5000:
        currencies_table['money_swis'] = str((conversion_swis - 5000) / 90)
        currencies_table.update()
      elif conversion_inr > 5000:
        currencies_table['money_inr'] = str((conversion_inr - 5000) / 1)
        currencies_table.update()
      else:
        alert("insufficient funds")


    def link_8_click(self, **event_args):
      open_form('deposit',user= self.user)
  
    def link_10_click(self, **event_args):
      open_form('withdraw',user= self.user)

    def link_1_click(self, **event_args):
      open_form('customer', user= self.user)

    def link_9_click(self, **event_args):
      open_form('transfer',user= self.user)
  
