import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import time
import json

HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

vacancies = []


def get_headers():
    return Headers(browser='chrome', os='win').generate()


def get_info_of_vacancy(href, city):
    search_param = ['Django', 'Джанго', 'Flask', 'Фласк']
    vacancy_info = []
    vacancy_page = requests.get(href, headers=get_headers())
    soup = BeautifulSoup(vacancy_page.text, 'lxml')
    vacancy_description = soup.find('div', {'class': 'vacancy-section'}).text
    for p in search_param:
        if p in vacancy_description:
            vacancy_title = soup.find('h1', {'class': 'bloko-header-section-1', 'data-qa': 'vacancy-title'}).text
            vacancy_info.append(vacancy_title)
            vacancy_info.append(city)
            vacancy_salary = soup.find('div', {'data-qa': 'vacancy-salary'}).find('span', {
                'class': 'bloko-header-section-2 bloko-header-section-2_lite'}).text
            vacancy_info.append(vacancy_salary)
            company_element = soup.find('div', {'class': 'vacancy-company-details'})
            company_name = company_element.find('span', {'class': 'vacancy-company-name'}).text.strip()
            vacancy_info.append(company_name)
            vacancy_info.append(href)
            vacancy_info[2] = vacancy_info[2].replace('\xa0', ' ')
            vacancy_info[3] = vacancy_info[3].replace('\xa0', ' ')
            return vacancy_info
    time.sleep(2)


def create_json(date):
    vacancy_dict = {
        'vacancy_title': date[0],
        'city': date[1],
        'vacancy_salary': date[2],
        'company_name': date[3],
        'href': date[4]
    }
    vacancies.append(vacancy_dict)

    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)


search_page = requests.get(HOST, headers=get_headers())
soup = BeautifulSoup(search_page.text, 'lxml')
all_vacancy = soup.findAll('div', class_='vacancy-serp-item__layout')

for vacancy in all_vacancy:
    vacancy_city = vacancy.find('div', {'class': 'bloko-text',
                                        'data-qa': 'vacancy-serp__vacancy-address'}).text.split(', ')[0]
    first_href = vacancy.find('a')['href']
    info_of_vacancy = get_info_of_vacancy(first_href, vacancy_city)
    if info_of_vacancy:
        create_json(info_of_vacancy)
    time.sleep(2)
