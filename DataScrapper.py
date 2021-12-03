import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.api import get

reviewlist = []
movieslist = []

list_url = 'https://www.beyazperde.com/filmler-tum/'
main_url = 'https://www.beyazperde.com'
sub_link_to_reviews ='kullanici-elestirileri/'

def get_soup(url):
  # Sending url to splash server
  r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
  # Creating BeautifulSoup object
  soup = BeautifulSoup(r.text, 'html.parser')
  return soup


# returns the list of the movies from one page
def get_movie_list(soup):
  movieCards = soup.find_all('li',{'class': 'mdl'})
  for card in movieCards:
    link = card.find('a', {'class': 'meta-title-link'})['href']
    movieslist.append(link)


# uses get_movie_list function 
# iterates over the pages passed as range to the function
def pagination_movie_list(soup, n1, n2):
  for x in range(n1, n2):
    get_movie_list(soup)
    if not soup.find('span', {'class': 'button button-md button-primary-full button-right button-disabled'}):
      pass
    else:
      break

# single movie reviews for one page
def get_reviews(soup):
  # Title of the movie
  title = soup.find('div', {'class': 'titlebar-title'})
  # Reading review cards
  reviews = soup.find_all('div', {'class': 'hred review-card cf'})

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



# soup = get_soup(temp_url)
# get_reviews(soup)
# print(len(reviewlist))
# print(reviewlist)


# pagination for one movie
# first version
def pagination_movie_reviews(movie_soup_string, n1, n2):
  for x in range(n1, n2):  
    movie_soup_string_new = ''
    if (x > 1):
      movie_soup_string_new = movie_soup_string+ '?page=' + str(x) 
    review_soup = get_soup(movie_soup_string_new)
    get_reviews(review_soup)
    if not review_soup.find('span', {'class': 'button button-md button-primary-full button-right button-disabled'}):
      pass
    else:
      break

def writeToExcel():
  # printing the list to excel
    df = pd.DataFrame(reviewlist)
    df.to_excel("film_reviews.xlsx", index=False)
    print('Fin')


# for each item in movie list
# first: add the review page substring
# second: add the page substring
def main():
  list_soup = get_soup(list_url)
  pagination_movie_list(list_soup, 1, 5)
  print("pagination movie list size: " + str(len(movieslist)))
  for item in movieslist:
    print("current item from movie list >> " + str(item))
    temp_string = str(main_url + item + sub_link_to_reviews)
    pagination_movie_reviews(temp_string, 1, 99)
    print("pagination review list size: " + str(len(reviewlist)))

  writeToExcel()


main()


#  NOT WORKING

# def getReviewNextPage(soup):
#   page = soup.find('nav', {'class': 'pagination cf'})
#   if not soup.find('span', {'class': 'button button-md button-primary-full button-right button-disabled'}):
#     sub_url = soup.find('a', {'class': 'xXx button button-md button-primary-full button-right'}, ['href'])


# soup = get_soup('https://www.beyazperde.com/filmler/film-269758/kullanici-elestirileri/')
# sub_url = soup.find('a', {'class': 'xXx button button-md button-primary-full button-right'})['href']
# print(sub_url)

#  END NOT WORKIGN