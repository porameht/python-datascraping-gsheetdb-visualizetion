import gspread

gc = gspread.service_account(filename="creds.json")
sh = gc.open('python-datascraping').sheet1

sh.append_row(['first','second','third'])