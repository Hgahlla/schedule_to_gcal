import requests
from bs4 import BeautifulSoup
from gcal_setup import convert_str_to_datetime
from gcal_setup import add_time
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

        # date = soup.find('span', {'id': 'ctl00_Body_lblDates'})
        # print(date.text)

        table = soup.find('table', {'id': 'scheduleTable'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        shifts = {}

        for row in rows:
            table_data = row.find_all('input')

            for day in table_data:
                cancel = day.get('data-canceldescription')
                shift_type = day.get('value')
                date = day.get('data-date')

                if not cancel:
                    if shift_type == 'P' or shift_type == 'SP':
                        dt = convert_str_to_datetime(date) + add_time(19)
                        iso_dt = dt.isoformat()
                        shifts[iso_dt] = [dt, shift_type]

        return shifts
