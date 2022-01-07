import os

from redis import StrictRedis
from Redis_cache import RedisCache
from bs4 import BeautifulSoup

if __name__ == '__main__':
    cache = RedisCache()
    r = StrictRedis(host='localhost', port=6379, db=0)
    if os.path.exists('Scraping_results.txt'):
        os.remove('Scraping_results.txt')
    file = open('Scraping_results.txt', 'a')
    no_chars = file.write('Title | Author | Rating\n')
    file.close()
    for i in range(r.keys().__len__()):
        url = r.keys()[i]
        if url == b'https://www.goodreads.com/book/show/646462._' or url == b'seen:pidp' or url == b'depth:pidp':
            continue
        print(i)
        print(r.keys()[i])
        html = cache.__getitem__(r.keys()[i])['html']
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1', attrs={'id': 'bookTitle'})
        tmp = soup.find(attrs={'id': 'bookAuthors'})
        if tmp is not None:
            author = tmp.find(attrs={'itemprop': 'name'})
        rating = soup.find(attrs={'itemprop': 'ratingValue'})

        if title is None or author is None or rating is None:
            print('BAD SCRAPE')
            continue
        else:
            file = open('Scraping_results.txt', 'a')
            no_chars = file.write(title.get_text(strip=True) + " | " + author.text + " | " + rating.get_text(strip=True)+"\n")
            file.close()
