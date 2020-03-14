import json
from datetime import datetime
from sqlalchemy import create_engine, text
from dateutil.parser import parse
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from django.conf import settings
from celery.schedules import crontab
from app import celery_app
from ..serializers import GeneralStats, GeneralStatsSerializer


@celery_app.task(name="update-data")
def fech_data(*args, **kwargs):
    """
    sceduled task to
    scrap the data from https://www.worldometers.info/coronavirus/
    """
    webdriver = ChromeDriverManager().install()
    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--window-size=1920,1080')

    driver = Chrome(webdriver, options=opt)

    print("<<<<<<<<<<<<scrapping started >>>>>>>>>>>>>>>>>>>>> \n")
    url = 'https://www.worldometers.info/coronavirus/'
    driver.get(url)
    data = driver.find_element_by_class_name("content-inner")

    print("\n<<<<<<<<<<<Fetching general stats >>>>>>>>>>>>>>>>>>>>> \n")
    last_update = data.find_elements_by_xpath(
        "//*[contains(text(), 'Last updated:')]")[0].text
    total_cases = data.find_elements_by_css_selector(
        '[id*="maincounter-wrap"]')[0].find_element_by_tag_name('span').text
    death_cases = data.find_elements_by_css_selector(
        '[id*="maincounter-wrap"]')[1].find_element_by_tag_name('span').text
    recovery_cases = data.find_elements_by_css_selector(
        '[id*="maincounter-wrap"]')[2].find_element_by_tag_name('span').text
    active_cases = data.find_elements_by_css_selector(
        '[class*="panel panel-default"]')[0]
    closed_cases = data.find_elements_by_css_selector(
        '[class*="panel panel-default"]')[1]
    currently_infected = active_cases.find_element_by_class_name(
        "number-table-main").text
    cases_with_outcome = closed_cases.find_element_by_class_name(
        "number-table-main").text
    mild_condition_active_cases = active_cases.find_elements_by_css_selector(
        '[class*="number-table"]')[1].text
    critical_condition_active_cases = active_cases.find_elements_by_css_selector(
        '[class*="number-table"]')[2].text
    recovered_closed_cases = closed_cases.find_elements_by_css_selector(
        '[class*="number-table"]')[1].text
    death_closed_cases = closed_cases.find_elements_by_css_selector(
        '[class*="number-table"]')[2].text
    general_stats = {
        'total_cases': ''.join(total_cases.split(',')),
        'death_cases': ''.join(death_cases.split(',')),
        'recovery_cases': ''.join(recovery_cases.split(',')),
        'currently_infected': ''.join(currently_infected.split(',')),
        'cases_with_outcome': ''.join(cases_with_outcome.split(',')),
        'mild_condition_active_cases': ''.join(mild_condition_active_cases.split(',')),
        'critical_condition_active_cases': ''.join(critical_condition_active_cases.split(',')),
        'recovered_closed_cases': ''.join(recovered_closed_cases.split(',')),
        'death_closed_cases': ''.join(death_closed_cases.split(',')),
        'last_update': parse(last_update.split('Last updated:')[1])
    }

    gen_serializer = GeneralStatsSerializer(data=general_stats)
    gen_serializer.is_valid(raise_exception=True)
    gen_serializer.save()

    print("<<<<<<<<<<<Fetching country stats >>>>>>>>>>>>>>>>>>>>> \n")

    country_data = driver.find_element_by_id('main_table_countries_today')
    country_data_list = country_data.find_element_by_tag_name(
        'tbody').find_elements_by_tag_name("tr")

    attributes = ['country', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered',
                  'active_cases', 'serious_critical', 'cases_per_mill_pop']

    engine = create_engine(
        f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:5432/{settings.DB_NAME}")
    print("<<<<<<<<<<<Persist to DB:START >>>>>>>>>>>>>>>>>>>>> \n")
    for country in country_data_list:
        country_stats = []
        for i in country.find_elements_by_tag_name("td"):
            country_stats.append(''.join(i.text.split(',')))

        detail = dict(zip(attributes, country_stats))
        country_ = detail['country']
        flag = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/International_Flag_of_Planet_Earth.svg/800px-International_Flag_of_Planet_Earth.svg.png"
        with open(settings.FLAGS_FILE, "r") as read_file:
            data = json.load(read_file)
            try:
                flag = data[country_]
            except:
                pass

        total_cases = detail['total_cases']
        new_cases = detail['new_cases'].split('+')[::-1][0]
        total_deaths = detail['total_deaths']
        new_deaths = detail['new_deaths'].split('+')[::-1][0]
        total_recovered = detail['total_recovered']
        active_cases = detail['active_cases']
        serious_critical = detail['serious_critical']
        cases_per_mill_pop = detail['cases_per_mill_pop']
        last_update = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        update_sql = f"""
        INSERT INTO cases_countrycases
        values (
            '{country_}', '{total_cases if total_cases else 0}',
            '{new_cases if new_cases else 0}', '{total_deaths if total_deaths else 0}',
            '{new_deaths if new_deaths else 0}', '{total_recovered if total_recovered else 0}',
            '{active_cases if active_cases else 0}', '{serious_critical if serious_critical else 0}',
            '{cases_per_mill_pop if cases_per_mill_pop else 0}', '{flag}', '{last_update}')
        ON CONFLICT (country) DO UPDATE SET
        total_cases = '{total_cases if total_cases else 0}',
        new_cases = '{new_cases if new_cases else 0}',
        total_deaths = '{total_deaths if total_deaths else 0}',
        new_deaths = '{new_deaths if new_deaths else 0}',
        total_recovered = '{total_recovered if total_recovered else 0}',
        active_cases = '{active_cases if active_cases else 0}',
        serious_critical = '{serious_critical if serious_critical else 0}',
        cases_per_mill_pop = '{cases_per_mill_pop if cases_per_mill_pop else 0}',
        flag = '{flag}',
        last_update = '{last_update}'
        """
        with engine.begin() as conn:  # TRANSACTION
            conn.execute(text(update_sql))
    print("<<<<<<<<<<<Persist to DB:END >>>>>>>>>>>>>>>>>>>>> \n")

    driver.quit()


celery_app.conf.beat_schedule = {
    # Execute every three hours.
    'add-every-three-hours': {
        'task': 'update-data',
        'schedule': crontab(minute='*/30'),
    },
}
