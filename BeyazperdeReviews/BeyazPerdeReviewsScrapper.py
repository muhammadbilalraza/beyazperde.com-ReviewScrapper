import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.api import get

reviewlist = []
movieslist = []

list_url = 'https://www.beyazperde.com/filmler-tum/'
main_url = 'https://www.beyazperde.com'
sub_link_to_reviews ='elestiriler-beyazperde/'

# Status: OK
def get_soup(url):
  # Sending url to splash server
  r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
  # Creating BeautifulSoup object
  soup = BeautifulSoup(r.text, 'html.parser')
  return soup

# Status: OK
def get_movie_list(soup):
  movieCards = soup.find_all('li',{'class': 'mdl'})
  for card in movieCards:
    link = card.find('a', {'class': 'meta-title-link'})['href']
    # print("Link in get_movie_list: " + str(link))
    movieslist.append(link)

# Status: OK
def pagination_movie_list(soup_string, n1, n2):
  for x in range(n1, n2):
    # print("Page in pagination_movie_list: " + str(x))
    if x == 1 : 
      get_movie_list(get_soup(soup_string))
    else:
      current_soup = get_soup(soup_string + "?page=" + str(x)) 
      if not (current_soup.find('span', {'class': 'button button-md button-primary-full button-right button-disabled'})):
        get_movie_list(current_soup)
      else:
        get_movie_list(current_soup)
        break


# Status: OK
def get_bp_review(soup):
  try:
    review = {
      'title': soup.find('div', {'class': 'titlebar-title'}).text.strip(),
      'rating' : float(soup.find('span', {'class': 'note'}).text.strip().replace(',', '.')),
      'review' : soup.find('div', {'class': 'editorial-content'}).text.strip()
    }
    reviewlist.append(review)
  except:
    pass


# Status: OK
def writeToExcel():
  # printing the list to excel
  print('\n---------------------\nPrinting to excel sheet...')
  df = pd.DataFrame(reviewlist)
  df.to_excel("official_reviews.xlsx", index=False)
  print('Finished')


# Status: OK
# def if_tab_active(soup):
#   for item in soup.body.main.nav.find_all('span', {'class': 'item js-item-mq-medium inactive'}):
#     if (item.find('div', string = "Beyazperde Eleştirisi")): 
#        return False
#   return True

# Status: OK
def if_tab_exist(soup):
  for item in soup.find_all('div', {'class': 'item-center'}):
    if (item.get_text() == 'Beyazperde Eleştirisi'):
      return True
  return False
  


def scrape_bp_reviews(start_page, end_page):
  print("Getting movies list...")
  pagination_movie_list(list_url, start_page, end_page)
  print("\n=> Total Movie List Size: " + str(len(movieslist)) + "\n")

  count = 0
  for item in movieslist:
    # print("Current Movie >> " + str(item))
    print('---------------------\nCurrent Movie URL >> ' + str(main_url + item))

    movie_url_soup = get_soup(main_url+ item)
    tab_exist = if_tab_exist(movie_url_soup)
    # tab_active = if_tab_active(movie_url_soup)

    try: 
      if tab_exist:
      #  if tab_active:
       bp_review_url = str(main_url + item + sub_link_to_reviews)
       get_bp_review(get_soup(bp_review_url))
       count += 1
       print("Movie " + str(count))
       print("Reviews Collected: " + str(len(reviewlist)))
      #  else:
      #    count += 1
      #    print("Tab is not active for movie " + str(count))
      else:
        count += 1
        print("Tab does not exist for movie " + str(count))
    except: 
      print("Exception")
      pass

  writeToExcel()


scrape_bp_reviews(401, 501)