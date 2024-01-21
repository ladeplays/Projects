import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request



base_url = 'http://quotes.toscrape.com/'


book = dict()
max_quote = 0
min_quote = 12115
length = 0
totalLength = 0

tagbook = {}
max_tag = 0
total_tag = 0



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
for i in range(1,11):
    number = str(i)
    url = base_url + 'page/' + number+'/'
    req = Request(url, headers=headers)
    url = urlopen(req).read()
    soup = BeautifulSoup(url, 'html.parser')
    

    data = soup.findAll('span', class_='text')
    artist = soup.findAll('small', class_='author')
    tags = soup.findAll('a', class_='tag')


    quote = [v.text.split('``') for v in data]
    artist = [j.text.split(')') for j in artist]
    tags = [k.text.split('/') for k in tags]
#   print(quote)
    length = len(quote)
    for i in range(0,length):
        if artist[i][0] not in book:
            book[artist[i][0]] = 1
            
        else:
            book[artist[i][0]] +=1
        length += len(quote[i][0])

        if len(quote[i][0]) > max_quote:
            max_quote = len(quote[i][0])
            textMax = quote[i][0]
            author_max = artist[i][0]
        if len(quote[i][0]) < min_quote:
            min_quote = len(quote[i][0])
            textMin = quote[i][0]
            author_min = artist[i][0]
    
    totalLength += length

    for z in range(0,len(tags)):
        if tags[z][0] not in tagbook:
            tagbook[tags[z][0]] = 1
            
        else:
            tagbook[tags[z][0]] +=1       

#############################################################################################

################################################################
#print(tags[0][0])

#print(artist[9][0])
print(f'{soup.title.text}\n\n\n')
print("Author statistics")
print('-----------------------------------\n')
print(f'The number of quotes by each author: \n')
for i in book.values():
    if i > max_quote:
        max_quote = i
    if i < max_quote:
        min_quote = i

for key,value in enumerate(book.items()):
    print(f'{value[0]}: {value[1]} quote(s)')
print()
print(f'The longest quote was by {author_max}')
print(f'The shortest quote was by {author_min}')

####################################################################
total_sum = sum(book.values())
avg_length = totalLength/total_sum
print(f'\n\n\nQUOTE ANALYSIS')
print('-----------------------------------\n')
print(f'The average length of quotes is: {avg_length} characters\n')
print(f'The longest quote was by {author_max}, stating {textMax}\n')
print(f'The shortest quote was by {author_min}, stating {textMin}')
print()

########################################################################
## TAG ANALYSIS

for k in tagbook.values():
     if k > max_tag:
          max_tag = k

print(f'\nTAG ANALYSIS')
print('-----------------------------------\n')
for i,j in enumerate(tagbook.items()):
     if j[1] == max_tag:
         print(f'The most popular tag is "{j[0]}"')

tag_sum = sum(tagbook.values())

print(f'There were {tag_sum} total tags used across all quotes')

print(f'\nVISUALIZATION')
print('-----------------------------------\n')
import plotly.graph_objects as plt
from plotly.subplots import make_subplots
sorted_authors = sorted(book.items(), 
key=lambda x: x[1], reverse=True)
top10 = dict(sorted_authors[:10])
x1 = list(top10.keys())
y1 = list(top10.values())



sorted_tags = sorted(tagbook.items(), key=lambda x: x[1], reverse=True)
top10tags= dict(sorted_tags[:10])
x2= list(top10tags.keys())
y2 = list(top10tags.values())



image1 = make_subplots(rows=2, cols=1)
image1.add_trace(plt.Scatter(x=x1, y=y1, mode='markers',name = 'Top 10 authors'),row=1,col=1)


image1.add_trace(plt.Scatter(x=x2, y=y2, mode='markers',name='Top 10 Tags'),row=2,col=1)
image1.show()

