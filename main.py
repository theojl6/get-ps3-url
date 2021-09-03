# import statements
import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import io

"""TODO: add feature to choose pages"""

# URL of a WebPage
URL = "https://dlpsgame.org/category/ps3/"
# use HEADERS to avoid "405 METHOD NOT ALLOWED" error
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0"}

"""Gets the latest page number from HTML page source"""
def get_total_page():
  req = Request(url=URL, headers=HEADERS)
  html = urlopen(req).read()
  soup = BeautifulSoup(html, 'html.parser')
  tag = soup.find(class_="pages")
  pages = tag.string
  pages = pages.split(" ")[-1]
  return int(pages)



if __name__ == "__main__":

  last_page = get_total_page()
  errors = []
  with io.open("output.txt", "w", encoding="utf-8") as output: # Use io.open() with encoding="utf-8" to avoid error
    for page_number in range(1, last_page + 1):
      # Open the URL and read the whole page
      try:
        req = Request(url=URL + f"page/{page_number}/", headers=HEADERS)
        html = urlopen(req).read()
        # Parse the string
        soup = BeautifulSoup(html, 'html.parser')
        # Loop over tags with class_="post-title entry-title"
        for element in soup.find_all(class_="post-title entry-title"):
          a_tag = element.find('a') # Get <a> tags from selected tags
          output.write("{} --> LINK: {} \n".format(a_tag.string,a_tag.get('href')))
      except:
        errors.append(page_number)

  print(f"Errors encountered: {len(errors)}")
  print(f"The following pages had errors: {errors}")