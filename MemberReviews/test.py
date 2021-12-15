import requests
from bs4 import BeautifulSoup
from requests.api import get


def get_soup(url):
  # Sending url to splash server
  r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
  # Creating BeautifulSoup object
  soup = BeautifulSoup(r.text, 'html.parser')
  return soup


# check if the member reviews is of type <a/>
# if it is then fetch the information otherwise
# move to the iteration.
# https://www.beyazperde.com/filmler/film-133392/ Dune
# https://www.beyazperde.com/filmler/film-256880/ Spider-Man
# https://www.beyazperde.com/filmler/film-287213/kullanici-elestirileri/ 6 reviews
# soup = get_soup('https://www.beyazperde.com/filmler/film-287213/kullanici-elestirileri/')

# print(soup.nav) #prints all the spans within the navs

# anchors = soup.body.main.nav
# print("__________ Printing ANCHOR 1 __________ ")
# print(anchors)
# anchors = anchors.find_all('span', {'class': 'item js-item-mq-medium inactive'})
# print("__________ Printing ANCHOR 2 __________ ")
# print(anchors)



# print("\n\n\n\n__________ PRINTING LOOP RESULT __________ ")
# for anchor in soup.body.main.nav.find_all('span', {'class': 'item js-item-mq-medium inactive'}):
#   if (anchor.find('div', string = "Üye Eleştirileri")): 
#     print ("FOUND")






# soup = get_soup('https://www.beyazperde.com/filmler-tum/?page=1464')
# # print (soup.find('a', {'class': "xXx button button-md button-primary-full button-right"}))
# print(soup.find('span', {'class': 'button button-md button-primary-full button-right button-disabled'}))

# soup = get_soup('https://www.beyazperde.com/filmler/film-287213/kullanici-elestirileri/')
# if not soup.find('span', {'class': 'button button-md button-primary-full button-right button-disabled'}):
#   print ("ACTIVE")
# else:
#   if soup.find('span', {'class': 'button button-md button-primary-full button-right button-disabled'}) == None:
#     print('Class not found')
#   else: 
#     print('DISABLED')

# temp = soup.find('h2', {'class': 'titlebar-title titlebar-title-md'}).text.strip().split(' ', 1)[0]
# print (temp)

# https://www.beyazperde.com/filmler/film-287213/
# https://www.beyazperde.com/filmler/film-284646/
# https://www.beyazperde.com/filmler/film-269618/

soup = get_soup('https://www.beyazperde.com/filmler/film-133392')

# print(soup.body.main.nav.find_all('span', {'class': 'item js-item-mq-medium inactive'}))

print(soup.body.main.find_all('a'))



def check_if_member_reviews_active(soup):
  tab_active = True
  tab_exist = True

  temp_soup = soup.body.main.nav.find_all('span', {'class': 'item js-item-mq-medium inactive'})

  for anchor in temp_soup:
    if (anchor.find('div', string = "Üye Eleştirileri")): 
       tab_active = False
    else: tab_exist = False


  print('Tab exist: ' + str(tab_exist))
  print('Tab active: ' + str(tab_exist))

  return tab_exist and tab_active

# print(check_if_member_reviews_active(soup))