from ._anvil_designer import setTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class set(setTemplate):
  def __init__(self,user=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user


  def outlined_button_1_click(self, **event_args):
    setter = anvil.server.call('user_detail', self.user['username'],self.text_box_1.text)






  

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("deposit",user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("transfer",user=self.user)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("withdraw",user=self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("service",user=self.user)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer",user=self.user)

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Home")


 
