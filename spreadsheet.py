import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret_sheets.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Tinderella').sheet1

def insertMessage(messagesList):
    index = 2
    sheet.insert_row(messagesList, index)






