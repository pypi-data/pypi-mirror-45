from IPython.core.display import display, HTML
from IPython.lib.display import IFrame
from osbot_gsuite.apis.GSheets import GSheets
from osbot_gsuite.apis.sheets.API_Jira_Sheets_Create import API_Jira_Sheets_Create
from osbot_gsuite.apis.sheets.API_Jira_Sheets_Sync import API_Jira_Sheets_Sync
from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest

class Jp_GSheets():

    def __init__(self, file_id=None, sheet_name=None):
        self.gsuite_secret_id = 'gsuite_gsbot_user'
        self.file_id          = file_id
        self.sheet_name       = sheet_name
        self.gsheets          = GSheets               (self.gsuite_secret_id)
        self.gsheets_sync     = API_Jira_Sheets_Sync  (self.file_id,self.gsuite_secret_id)
        self.jira_api_rest    = API_Jira_Rest()
        #self.gsheets_create   = API_Jira_Sheets_Create(self.file_id)



    def metadata(self):
        return self.gsheets.sheets_metadata(self.file_id)

    def values(self):
        return self.gsheets.get_values_as_objects(self.file_id, self.sheet_name)

    def link(self):
        url = self.gsheets.gdrive.file_weblink(self.file_id)
        html = "Here is the <a href='{0}' target='_blank'>link</a> for the sheet with id <i>{1}</i>".format(url, self.file_id)

        display(HTML(html))

    def show(self, width='100%', height=400):
        url     = self.gsheets.gdrive.file_weblink(self.file_id)
        iframe  = IFrame(url,width=width,height=height)
        display(HTML("<style>.container { width:98% !important; }</style>"))
        display(iframe)




#%autoreload
#from osbot_jupyter.api_notebook.Jp_Helper import Jp_Helper
##Jp_Helper.trace_method(sheets.gsheets_sync.load_data_from_jira)