from ._anvil_designer import audit_trailTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class audit_trail(audit_trailTemplate):
  def __init__(self, user=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user
    self.action_info()
    self.repeating_panel_1.items = app_tables.actions.search()
   
  def action_info(self):
    
    if self.user is not None:
      user_info = anvil.server.call('add_info', self.user['username'], self.last_login['last_login'])
      app_tables.actions.add_row(
                username=user_info['username'],
                last_login=datetime.datetime.now().date(),
                changes=changes
            )

            

  def button_1_click(self, **event_args):
        entered_user = self.text_box_1.text
        filtered_actions = app_tables.actions.search(username=entered_user)
        self.repeating_panel_1.items = filtered_actions

  def link_8_click(self, **event_args):
    open_form('admin')

 
