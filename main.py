import asyncio
from anyio import TypedAttributeLookupError
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import gspread
import datetime


async def gethtml():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        # Login
        await page.goto("https://backoffice.nigoal939.com/login")
        await page.fill('input#username','aun')
        await page.fill('input#password','aun331930')
        await page.click('a#login')
        await page.wait_for_url("https://backoffice.nigoal939.com/Dashboard")
        print("Login successfully")

        # Logautobank
        await page.goto("https://backoffice.nigoal939.com/Logautobank")
        await page.wait_for_url("https://backoffice.nigoal939.com/Logautobank")
        await page.wait_for_timeout(3000)
        html_logautobank = await page.inner_html('main.page-content')
        print("Get data autobank successfully")
        
        # Withdrawcredit
        await page.goto("https://backoffice.nigoal939.com/Withdrawcredit")
        await page.wait_for_url("https://backoffice.nigoal939.com/Withdrawcredit")
        await page.wait_for_timeout(2000)
        await page.select_option('[aria-controls="depositTable"]', '100')
        await page.wait_for_timeout(2000)
        html_withdrawcredit = await page.inner_html('main.page-content')
        print("Get data withdraw successfully")
        return [html_logautobank, html_withdrawcredit]


def manipulate(html):
    j = 0
    arr_account = []
    soup = BeautifulSoup(html, 'html.parser')
    total_books = soup.find_all('h3', {'class':""})
    arr_book = [i.get_text().strip() for i in total_books]
    print(arr_book)
    for j in soup.find_all('h2'):
        data = j.text
        arr_account.append(data)
    print(arr_account)
    return [arr_book, arr_account]
    

def withdrawcredit(html):
    arr_transec = []
    table_headers = []
    table_rows = []
    soup = BeautifulSoup(html, 'html.parser')
    transec_deposit = soup.find('span',{'id':"depositTotalByDate"}).text
    transec_withdraw = soup.find('span',{'id':"withdrawTotalByDate"}).text
    arr_transec.append(transec_deposit)
    arr_transec.append(transec_withdraw)
    print(arr_transec)
    table_deposit = soup.find('table',{"id":"depositTable"})
    for k in table_deposit.find_all('th'):
        title = k.text
        table_headers.append(title)
    for m in table_deposit.find_all('tr')[1:]:
        row_data = m.find_all('td')
        row = [n.text for n in row_data]
        table_rows.append(row)
    return [table_headers, table_rows]    
        
          
def check_data(data):
    count_table = 0
    arr_value_status = []
    sum_arr_value_status = 0

    for x in range(len(data)):
        data_status_deposit = data[count_table][14]
        data_value_status_deposit = data[count_table][7]
        
        if data_status_deposit == "บอทไม่ดึง":
            arr_value_status.append(data_value_status_deposit)
            print("notification")
        elif data_status_deposit == "เติมเงินไม่เข้า":
            arr_value_status.append(data_value_status_deposit)
            print("notification two case")
        else:
            print("promotion")

        count_table += 1

    print(arr_value_status)
    print(len(arr_value_status))
    
    for z in arr_value_status:
        z = z.replace(",","")
        sum_arr_value_status += float(z)
    print(sum_arr_value_status)       

    
data = asyncio.run(gethtml())
datatable_withdrawcredit = withdrawcredit(data[1])
manipulate(data[0])
check_data(datatable_withdrawcredit[1])



 




