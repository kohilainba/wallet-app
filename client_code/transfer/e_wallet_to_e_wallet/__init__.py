from ._anvil_designer import e_wallet_to_e_walletTemplate
from anvil import *
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
        depoitor = self.text_box_1.text
        wallet_id = self.text_box_2.text
        transfer_amount = self.text_box_3.text
        depositor_wallet_id= anvil.server.call('generate_unique_id', self.user['username'], self.user['phone'])
        #getting the depositor's details
        fore_money_depositor = anvil.server.call('get_accounts_emoney_using_wallet_id', depositor_wallet_id)
        #getting the reciever's details
        fore_money_sent = anvil.server.call('get_accounts_emoney_using_wallet_id',wallet_id)

        if (transfer_amount < 5) or (transfer_amount > 50000):
           self.label_4.text = "Tran should be between 5 and 50000 for a transfer Funds." 
        else:
           #calculating the money to be added in the recieve's end
           transfer_fianl_sent_amount= float(fore_money_sent['e_money']) + transfer_amount
           #calculating the money to be deducted in the depositor's end
           transfer_amount_final = float(fore_money_depositor['e_money'])-transfer_amount
           #setting the value
           anvil.server.call('update_rows_emoney_trasaction',depositor_wallet_id, str(transfer_amount_final))
           anvil.server.call('update_rows_emoney_trasaction',wallet_id, str(transfer_fianl_sent_amount))
           self.label_4.text = "Money transferred successfully"
           
      
        
        

        # if (transfer_amount < 5) or (transfer_amount > 50000):
        #   self.label_4.text = "Money value should be between 5 and 50000 for a transfer Funds."  
        # else:  
        #    if from_user_emoney is not None and to_user_emoney is not None:
        #      if float(from_user_emoney['e_money']) >= transfer_amount:
        #       from_user_emoney['e_money'] = str(float(from_user_emoney['e_money']) - transfer_amount)
        #       to_user_emoney['e_money'] = str(float(to_user_emoney['e_money']) + transfer_amount)
        #       anvil.server.call('update_all_rows', from_user_ewallet, user_for_emoney)
        #       anvil.server.call('update_all_rows', to_user_ewallet, user_for_emoney)

        #       app_tables.transactions.add_row(
        #         user=self.user,
        #         e_wallet=from_user_ewallet,
        #         money=f"Transfer-{transfer_amount}",
        #         date=current_datetime,
        #         transaction_type="E-wallet to E-wallet"
        #       )

        #       app_tables.transactions.add_row(
        #         user=self.user,
        #         e_wallet=to_user_ewallet,
        #         money=f"Transfer-{transfer_amount}",
        #         date=current_datetime,
        #         transaction_type="E-wallet to E-wallet"
        #       )
        #      else:
        #        self.label_4.text="insufficient fund"
        #    else:
        #        self.label_4.text="Error retrieving e-money information"

    def link_8_click(self, **event_args):
      open_form('deposit',user= self.user)
  
    def link_10_click(self, **event_args):
      open_form('withdraw',user= self.user)

    def link_1_click(self, **event_args):
      open_form('customer', user= self.user)

    def link_9_click(self, **event_args):
      open_form('transfer',user= self.user)
  
