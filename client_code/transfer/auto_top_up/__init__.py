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
        anvil.server.call('update_all_rows',self.user['username'], final)
        self.deduct_currencies(final)
      else:
        return f"E-wallet balance ({money_in_emoney}) is above the threshold. No top-up needed."
    self.button_1.visible = False
    self.button_2.visible = True

  def deduct_currencies(self, amount):
    currencies_table = app_tables.currencies.get(user=self.user['username'])
    if currencies_table['money_usd'] > 200:
        conversion = float(currencies_table['money_usd'])*80
        currencies_table['money_usd'] = str((conversion- 5000)/80)
        currencies_table.update()
    elif currencies_table['money_euro'] > 200:
        conversion = float(currencies_table['money_euro'])*85
        currencies_table['money_euro'] = str((conversion- 5000)/85)
        currencies_table.update()
    elif currencies_table['money_swis'] > 200:
        conversion = float(currencies_table['money_swis']) * 90
        currencies_table['money_swis'] = str((conversion - 5000) / 90)
        currencies_table.update()
    elif currencies_table['money_inr'] > 5000:
        conversion = float(currencies_table['money_inr']) * 1  
        currencies_table['money_inr'] = str((conversion - 5000) / 1)
        currencies_table.update()
    else:
      alert("insufficient funds")
    

  def button_2_click(self, **event_args):
    self.user['top_up']= False
    self.user.update()
    self.button_1.visible = True
    self.button_2.visible = False
