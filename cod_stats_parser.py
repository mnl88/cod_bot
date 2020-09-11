"""
Парсер с сайта https://cod.tracker.gg/

"""
import requests
from bs4 import BeautifulSoup


HOST = 'https://cod.tracker.gg/'
URL_MP_START = 'modern-warfare/profile/atvi/'
URL_MP_FINISH = '/mp'
URL_WZ_START = 'warzone/profile/atvi/'
URL_WZ_FINISH = '/overview'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
              'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}



def get_html(host, url_start, url_finish, activision_id: str):
    """распарчим страничку"""
    url_middle = activision_id.replace('#', '%23')
    url = host + url_start + url_middle + url_finish
    response = requests.get(url=url, headers=HEADERS)
    return response


def get_content(html, game_type='WZ'):
    """Вернем список труб"""
    if game_type == 'WZ':
        kd_ratio_column = 2
    else:
        kd_ratio_column = 0

    soup = BeautifulSoup(html.text, 'html.parser')  # превращаем HTML в суп
    try:
        mini_soup = soup.find('div', class_='giant-stats')  # уменьшаем суп до таблицы
        items = mini_soup.find_all('div', class_='stat align-left giant expandable')  # разбиваем построчно
        for i, item in enumerate(items[:3]):  # перебирает только строк в каждом блоке
            if i == kd_ratio_column:
                title = item.find('span', title='K/D Ratio').get_text()
                if title == 'K/D Ratio':
                    kd_ratio = item.find('span', class_='value').get_text()
                    return kd_ratio
    except:
        pass


def parser_act_id(activision_id, game_type='WZ'):
    """парсер КД по id activision"""
    if game_type == 'WZ':
        html = get_html(HOST, URL_WZ_START, URL_WZ_FINISH, activision_id)
    else:
        html = get_html(HOST, URL_MP_START, URL_MP_FINISH, activision_id)
    if html.status_code == 200:
        kd_ratio = get_content(html, game_type)
        return kd_ratio
    else:
        print('Error')


def main():
    activision_id = 'Dikiy_Kaban#236583348'
    kd_wz = parser_act_id(activision_id, 'WZ')
    kd_mp = parser_act_id(activision_id, 'MP')
    print(kd_wz, kd_mp)


if __name__ == '__main__':
    main()
