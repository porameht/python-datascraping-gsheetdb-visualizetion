from cgitb import text
from functools import cache
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import gspread




while True:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://backoffice.nigoal939.com/login")
        page.fill('input#username','aun')
        page.fill('input#password','aun331930')
        page.click('a#login')
        page.wait_for_timeout(10000)
        page.is_visible("div.ml-auto")
        html = page.inner_html('main.page-content')
        soup = BeautifulSoup(html, 'html.parser')
        totalBooks = soup.find_all('h3', {'class':""})
        arrAccount = []
        for j in range(4):
            j = j + 1
            totalAccount = soup.find('h3', {'class':"text-muted tg"+str(j)}).text
            arrAccount.append(totalAccount) 
        arrBook = [i.get_text().strip() for i in totalBooks]

        print(arrBook)
        print(arrAccount)
        
        gc = gspread.service_account(filename="creds.json")
        sh = gc.open('python-datascraping').sheet1
        sh.append_row(['first','second','third'])



 




