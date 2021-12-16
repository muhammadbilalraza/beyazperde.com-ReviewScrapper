import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.api import get

reviewlist = []
movieslist = []

list_url = 'https://www.beyazperde.com/filmler-tum/'
main_url = 'https://www.beyazperde.com'
sub_link_to_reviews ='kullanici-elestirileri/'

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
    print("Link in get_movie_list: " + str(link))
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
# single movie reviews for one page
def get_reviews(soup):
  # Title of the movie
  title = soup.find('div', {'class': 'titlebar-title'})
  # Reading review cards
  reviews = soup.find_all('div', {'class': 'hred review-card cf'})

  reviews_len = len(reviewlist)

  try: 
    for item in reviews:
      review = {
      'title': title.text.strip(),
      'person_name' : item.find('div', {'class': 'meta-title'}).text.strip(),
      'rating' : float(item.find('span', {'class': 'stareval-note'}).text.replace(',','.').strip()),
      'body' : item.find('div', {'class': 'content-txt review-card-content'}).text.strip(),
      }
      reviewlist.append(review)
  except:
    pass

  return len(reviewlist) - reviews_len


# Status: OK
# pagination for one movie
def pagination_movie_reviews(movie_soup_string, n1, n2):
  count_reviews = int(get_soup(movie_soup_string).find('h2', {'class': 'titlebar-title titlebar-title-md'}).text.strip().split(' ', 1)[0])
  print('COUNT REVIEWS: ' + str(count_reviews))
  read_reviews = 0
  for x in range(n1, n2):  
    print('Movie Reviews Iteration: ' + str(x))
    print ('Movie Reviews Collected: ' + str(len(reviewlist)))
    movie_soup_string_new = ''
    # for url page=id
    if (x > 1):
      movie_soup_string_new = movie_soup_string+ '?page=' + str(x) 
    else: 
      movie_soup_string_new = movie_soup_string

    review_soup = get_soup(movie_soup_string_new)
    read_reviews += get_reviews(review_soup)


    print("Read reviews: " + str(read_reviews))
    if(read_reviews == count_reviews):
      break


    if not review_soup.find('span', {'class': 'button button-md button-primary-full button-right button-disabled'}):
      pass
    else:
      break


# Status: OK
def writeToExcel():
  # printing the list to excel
    df = pd.DataFrame(reviewlist)
    df.to_excel("film_reviews.xlsx", index=False)
    print('Fin')


# Status: OK
def check_if_member_reviews_tab_exist_and_active(soup):
  tab_active = True
  tab_exist = True

  for anchor in soup.body.main.nav.find_all('span', {'class': 'item js-item-mq-medium inactive'}):
    if (anchor.find('div', string = "Üye Eleştirileri")): 
       tab_active = False
    else: tab_exist = False

  return tab_exist and tab_active
  

def scrape_member_reviews(start_page, end_page):
  pagination_movie_list(list_url, start_page, end_page)
  # print("Total Movie List Size: " + str(len(movieslist)))

  for item in movieslist:
    # print("Current Movie >> " + str(item))
    # print('Movie URL >> ' + str(main_url + item))

    movie_url_soup = get_soup(main_url+ item)
   
    try: 
      if check_if_member_reviews_tab_exist_and_active(movie_url_soup):
       member_review_url = str(main_url + item + sub_link_to_reviews)
      #  print('Member Review URL >> ' + member_review_url)
       pagination_movie_reviews(member_review_url, 1, 999)
      #  print("Reviews Collected: " + str(len(reviewlist)))
      else:
        continue
    except: 
      pass

  writeToExcel()


scrape_member_reviews(1, 101)
