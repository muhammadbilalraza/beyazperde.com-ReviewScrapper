from bs4.element import SoupStrainer
import requests
from bs4 import BeautifulSoup
from requests.api import get



# url = 'https://www.beyazperde.com/filmler/film-269758/elestiriler-beyazperde/'
url = 'https://www.beyazperde.com/filmler/film-254994/'

def get_soup(url):
  # Sending url to splash server
  r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
  # Creating BeautifulSoup object
  soup = BeautifulSoup(r.text, 'html.parser')
  return soup
  


# soup = get_soup(url)
# tab = soup.find_all('div', {'class': 'item-center'})
# for item in tab:
#   if (item.get_text() == 'Beyazperde Eleştirisi'):
#     print(item.get_text())


# soup = get_soup('https://www.beyazperde.com/filmler/film-269758/elestiriler-beyazperde/')
# anchor = soup.main.nav.find_all('a')
# print(anchor)
# for item in anchor:
#   if(item.find('div', {'class': 'item-center'}).text.strip() == 'Beyazperde Eleştirisi'):
#     print ("FOUND")


soup = get_soup('https://www.beyazperde.com/filmler/film-261255/')
def if_tab_exist(soup):
  for item in soup.find_all('div', {'class': 'item-center'}):
    if (item.get_text() == 'Beyazperde Eleştirisi'):
      return True
  return False


def if_tab_active(soup):
  for item in soup.body.main.nav.find_all('span', {'class': 'item js-item-mq-medium inactive'}):
    if (item.find('div', string = "Beyazperde Eleştirisi")): 
       return False
  return True


try: 
    if tab_exist:
      if tab_active:

      else:
        count += 1
        print("Tab is not active for movie " + str(count))
    else:
      count += 1
      print("Tab does not exist for movie " + str(count))
except: 
  print("Exception")
  pass

print(if_tab_exist(soup))
print(if_tab_active(soup))
