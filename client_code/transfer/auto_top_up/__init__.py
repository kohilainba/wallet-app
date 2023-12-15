from ._anvil_designer import auto_top_upTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class auto_top_up(auto_top_upTemplate):
  def __init__(self, user=None, **properties):
    self.user = user
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    user_account_numbers = anvil.server.call('get_user_account_numbers', self.user['username'])
    self.dropdown_account_numbers.items = user_account_numbers
    self.button_2.visible= False


  def link_8_click(self, **event_args):
    open_form('deposit',user= self.user)

  def link_10_click(self, **event_args):
    open_form('withdraw',user= self.user)

  def link_1_click(self, **event_args):
    open_form('customer', user= self.user)

  def link_9_click(self, **event_args):
    open_form('transfer',user= self.user)

  def button_1_click(self, **event_args):
    self.user['top_up']= True
    self.user.update()
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
    

  def button_2_click(self, **event_args):
    self.user['top_up']= False
    self.user.update()
    self.button_1.visible = True
    self.button_2.visible = False
