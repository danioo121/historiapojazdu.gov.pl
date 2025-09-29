from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

def znajdz_d1r(rejestracja, vin, rocznik):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = 'https://historiapojazdu.gov.pl/'
        date_obj = datetime.strptime(f'0101{rocznik}', "%d%m%Y")

        while int(date_obj.strftime('%Y')) == rocznik:
            date_str = date_obj.strftime("%d%m%Y")
            page.goto(url)

            page.fill('input[id*=":rej"]', rejestracja)
            page.fill('input[id*=":vin"]', vin)
            page.fill('input[id*=":data"]', date_str)
            page.click('input[id*=":btnSprawdz"]')

            page.wait_for_timeout(3000)  # poczekaj 3 sekundy

            if 'oś czasu' in page.content().lower():
                browser.close()
                return date_str

            date_obj += timedelta(days=1)

        browser.close()
        return False
