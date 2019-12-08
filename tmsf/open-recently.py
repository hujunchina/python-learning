import requests
from bs4 import BeautifulSoup
import sys
import os
import datetime

url = 'http://www.tmsf.com/newhouse/OpenReport_show_33.htm'

def get_page_content(url):
    req = requests.get(url)
    return req.text

def get_beautiful_soup(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup

def get_data_tables(soup):
    table_tags = soup.find_all('table')
    data_list = []
    for table in table_tags[:15]:
        tr_tags = table.find_all('tr')
        tr_name = tr_tags[0]
        tr_time = tr_tags[2]
        time = tr_time.ul.li.text
        name = tr_name.find('span')
        num = table.find('span','taoshu')
        #print(time)
        s = '{:一<10}'.format(name.text)+'{:-<15}'.format(num.text)+time+'\n'
        print(s)
        data_list.append(s)
    return data_list
        
def save_data(data_list):
    path_name = './data'
    file_name = str(datetime.date.today())+'-open-recently.txt'
    with open(os.path.join(path_name, file_name), 'w+') as f:
        f.writelines(data_list)
        f.close()
    
data_list = get_data_tables(get_beautiful_soup(get_page_content(url)))
save_data(data_list)

