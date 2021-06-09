import requests
from bs4 import BeautifulSoup
import secret

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

payload = {
    '__VIEWSTATE': secret.viewstate,
    '__VIEWSTATEGENERATOR': secret.viewstategenerator,
    '__EVENTVALIDATION': secret.eventvalidation,
    'ctl00$ContextMenu$hdnIsAliveToken': secret.token,
    'ctl00$Body$txtUsername': secret.username,
    'ctl00$Body$txtPassword': secret.password,
    'ctl00$Body$txtDomain': secret.domain,
    'ctl00$Body$btnSubmit': 'Login'
}

login_url = "https://northtexas.fs.app.medcity.net/Login.aspx"
schedule_url = secret.schedule_url


def get_schedule():
    with requests.session() as s:
        s.post(login_url, headers=headers, data=payload)
        res = s.get(schedule_url)
        soup = BeautifulSoup(res.text, 'html.parser')

        date = soup.find('span', {'id': 'ctl00_Body_lblDates'})
        #print(date.text)

        table = soup.find('table', {'id': 'scheduleTable'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        shift_dates = []

        for row in rows:
            table_data = row.find_all('input')

            for day in table_data:
                shift = day.get('value')
                if shift == 'P' or shift == 'SP':
                    #print(day.get('data-date'), shift)
                    shift_dates.append(day.get('data-date'))

        return shift_dates


if __name__ == '__main__':
    get_schedule()
