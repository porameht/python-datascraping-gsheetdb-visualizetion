import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import gspread
import datetime


async def getHtml():
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        await page.goto("https://backoffice.nigoal939.com/login")
        await page.fill('input#username','aun')
        await page.fill('input#password','aun331930')
        await page.click('a#login')
        await page.wait_for_timeout(20000)
        await page.goto("https://backoffice.nigoal939.com/login")
        await page.wait_for_selector('main.page-content')
        await page.is_visible("div.ml-auto")
        html = await page.inner_html('main.page-content')
        return html
    

def manipulate(html):
    arrAccount = []
    x = datetime.datetime.now()
    date = x.strftime("%x")
    time = x.strftime("%X")
    arrAccount.append(date)
    arrAccount.append(time)
    soup = BeautifulSoup(html, 'html.parser')
    totalBooks = soup.find_all('h3', {'class':""})
    for account in range(len(totalBooks)):
        account += 1
        totalAccount = soup.find('h3', {'class':"text-muted tg"+str(account)}).text
        arrAccount.append(totalAccount) 
    arrBook = [i.get_text().strip() for i in totalBooks]
    allData = arrAccount + arrBook
    return allData

def output(allData):
    gc = gspread.service_account(filename="creds.json")
    sh = gc.open('python-datascraping').sheet1
    sh.append_row(allData)
    return

while True:
    data = asyncio.run(getHtml())
    sumalize = manipulate(data)
    output(sumalize)




 




