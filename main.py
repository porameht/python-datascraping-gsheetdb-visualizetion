import asyncio
from anyio import TypedAttributeLookupError
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
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
        # Logautobank
        await page.goto("https://backoffice.nigoal939.com/Logautobank")
        await page.wait_for_url("https://backoffice.nigoal939.com/Logautobank")
        await page.wait_for_timeout(1000)
        await page.click('a#deposit_manual-tab')
        await page.wait_for_timeout(3000)
        # text = await page.inner_html('div.tab-pane fade')
        table = await page.inner_text('table')
        html = await page.inner_html('main.page-content')
        # print(text)
        print(table)
        # Withdrawcredit
        await page.goto("https://backoffice.nigoal939.com/Withdrawcredit")
        await page.wait_for_url("https://backoffice.nigoal939.com/Withdrawcredit")
        await page.wait_for_timeout(3000)
        html1 = await page.inner_html('main.page-content')

        return [html, html1]


def manipulate(html):
    j = 0
    arr_account = []
    arr_table = []
    soup = BeautifulSoup(html, 'html.parser')
    total_books = soup.find_all('h3', {'class':""})
    arr_book = [i.get_text().strip() for i in total_books]
    # trans_success = soup.find('h2').text
    # trans_success = soup.find_all('h2')
    # spans = soup.find_all('span', {'class' : 'fa fa-credit-card f-left'})
    for j in range(len(arr_book)):
        trans_success = soup.find_all('h2')
        data = trans_success[j].text
        arr_account.append(data)
        j += 1

    for i in range(18):
        # data_table = soup.find_all('tr')
        data_table = soup.find_all('p',{'class':"text-right"})
        result_table = data_table[i].text
        arr_table.append(result_table)


    # print(arr_table)
    print(arr_book)
    print(arr_account)
    

def withdrawcredit(html):
    arr_transec = []
    soup = BeautifulSoup(html, 'html.parser')
    transec_deposit = soup.find('span',{'id':"depositTotalByDate"}).text
    transec_withdraw = soup.find('span',{'id':"withdrawTotalByDate"}).text
    arr_transec.append(transec_deposit)
    arr_transec.append(transec_withdraw)
    print(arr_transec)






data = asyncio.run(gethtml())
manipulate(data[0])
withdrawcredit(data[1])



 




