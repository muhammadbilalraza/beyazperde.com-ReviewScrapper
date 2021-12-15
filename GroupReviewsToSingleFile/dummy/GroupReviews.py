import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font


df = pd.read_excel('1001_1100_pages.xlsx')

# get a list of unique movie names
movielist = []
filter_by_first_col = df.drop_duplicates(subset=['title']).iloc[:, 0]
for movie in filter_by_first_col:
  movielist.append(movie)

# grouping by the movie title and printing each group
id = 1
review = 1

for movie in movielist:
  wb = Workbook()

  # reading tuples based on movie title
  grouped = df.groupby('title').get_group(movie)

  # writing tuple to worksheet
  for row in grouped.itertuples():
    # creating new worksheet
    ws = wb.create_sheet(f'{review}')
    # writing header
    ws.append(list(df.keys()))
    values = [row[1], row[2], row[3], row[4]]
    ws.append(values)
    print(ws)


    if (review==1):
      del wb['Sheet']
    # incrementing to review
    review += 1

    
  review = 1

  wb.save(f'{id}.xlsx')
  id += 1


print("Finished")









# grouped = df.groupby('title').get_group(movielist[2])

# print(len(movielist))
# ids = range(1, len(movielist) + 1)
# for i in ids: 
#   print (i)


# values = list(df.groupby('title').get_group('Acı Tatlı Tesadüfler'))
# print(values)