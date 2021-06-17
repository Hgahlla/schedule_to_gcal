import requests
from bs4 import BeautifulSoup
import datetime
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


def get_schedule():
    s = requests.session()
    s.post(login_url, headers=headers, data=payload)

    # Current Month of Shifts
    sch_url = f"https://northtexas.fs.app.medcity.net/Schedule/EmployeeScheduleBrowse.aspx?FacilityId={secret.fac_id}&DepartmentId={secret.depart_id}&EmployeeId={secret.emp_id}"
    default_page = s.get(sch_url)
    def_soup = BeautifulSoup(default_page.text, 'html.parser')

    shifts = scrape_schedule(def_soup, shifts={})

    # Next Month of Shifts
    start_date = get_start_date(def_soup)
    next_sch_url = sch_url + f"&startDate={start_date.month}%2f{start_date.day}%2f{start_date.year}"
    next_page = s.get(next_sch_url)
    next_soup = BeautifulSoup(next_page.text, 'html.parser')

    shifts = scrape_schedule(next_soup, shifts)

    return shifts


def scrape_schedule(soup, shifts):
    table = soup.find('table', {'id': 'scheduleTable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        table_data = row.find_all('input')

        for day in table_data:
            cancel = day.get('data-canceldescription')
            shift_type = day.get('value')
            date = day.get('data-date')

            if shift_type == 'P' or shift_type == 'SP':
                dt = convert_str_to_datetime(date) + add_time(19)
                iso_dt = dt.isoformat()
                if not cancel:
                    shifts[iso_dt] = [dt, shift_type, False]
                else:
                    shifts[iso_dt] = [dt, shift_type, True]
    return shifts


def get_start_date(soup):
    dates = soup.find('span', {'id': 'ctl00_Body_lblDates'}).get_text()
    end_date = dates.split()[2]
    start_date = datetime.datetime.strptime(end_date, '%m/%d/%Y') + datetime.timedelta(days=1)
    return start_date
