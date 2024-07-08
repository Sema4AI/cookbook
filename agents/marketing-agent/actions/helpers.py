from sema4ai.actions import action
import requests
from bs4 import BeautifulSoup
import re
import json
import os

class BaseScraper:
      def __init__(self, url):
         self.response = requests.get(url)
         self.soup = BeautifulSoup(self.response.text, 'html.parser')
         self.parent_dir = "/tmp/tags"
   
      # children must override these methods
      def fetch_article_links(self, num_articles=10):
         raise NotImplementedError
   
      def scrape_article_content(self, article_url):
         raise NotImplementedError
      
      def save_article_content(self, filename, content):
         with open(filename, 'w+', encoding='utf-8') as file:
            file.write(content)
      
      def save_title(self, input_filename, path_to_save):
         filename = input_filename.split('/')[-1].split('.')[0].split('-')
         site = filename[0]
         title = filename[1:-1] if site == 'medium' else filename[1:]
         title = ' '.join(title)
         title = title.title()
         if not os.path.exists(path_to_save):
            with open(path_to_save, 'w+') as f:
               json.dump({}, f)
         with open(path_to_save, 'r') as f:
            data = json.load(f)
            if site not in data:
               data[site] = []
            data[site].append(title)
         with open(path_to_save, 'w+') as f:
            json.dump(data, f, indent=4)
         print(f"Title: {title} saved.")

      def get_parent_dir(self):
          return self.parent_dir

class TechCrunchScraper(BaseScraper):
   def __init__(self, tag):
      self.tag = tag.lower().replace(' ', '-')
      url = f'https://techcrunch.com/tag/{self.tag}/'
      super().__init__(url)
   
   def fetch_article_links(self, num_articles=10):
      figures = self.soup.find_all('figure', class_="wp-block-post-featured-image")

      # Define a regex pattern to match URLs that contain a year after the domain
      pattern = re.compile(r'https://techcrunch\.com/\d{4}/')

      # Initialize a list to store the links
      links = set()

      # Iterate over each figure found
      for figure in figures:
         if num_articles is not None and len(links) >= num_articles:
               break
         a_tag = figure.find('a', href=True)
         if a_tag and pattern.search(a_tag['href']):
               links.add(a_tag['href'])

      return links
   
   def scrape_article_content(self, article_url):
      response = requests.get(article_url)
      article_soup = BeautifulSoup(response.text, 'html.parser')

      # Find the main content div
      content_div = article_soup.find('div', class_='entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow')

      # Initialize an empty list to hold all text pieces
      article_content = []

      if content_div:
         # Extract text from all <p> tags and header tags
         text_elements = content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
         for element in text_elements:
            text = element.get_text(strip=True)
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                  # Add formatting for headers
                  article_content.append(f"**{text}**\n")
            else:
                  # Add text with a newline for paragraphs
                  article_content.append(f"{text}\n")

      # Join all pieces of text into a single string
      full_article = '\n'.join(article_content)
      return full_article
   
   def get_tag(self):
      return self.tag
   

class MediumScraper(BaseScraper):
   def __init__(self, tag):
      self.tag = tag.lower().replace(' ', '-')
      url = f'https://medium.com/tag/{self.tag}'
      super().__init__(url)

   def fetch_article_links(self, num_articles=10):
      # Find all <div> tags with the role="link"
      divs = self.soup.find_all('div', attrs={'role': 'link'})
      # print(divs)
      links = []

      # Iterate over each div found
      for div in divs:
         if num_articles is not None and len(links) >= num_articles:
            break
         # Check if 'link-href' attribute exists
         data_href = div.get('data-href')
         if data_href:
            # Append the full URL (considering relative URLs)
            full_url = f"https://medium.com{data_href}" if data_href.startswith('/') else data_href
            links.append(full_url)

      return links
   
   def scrape_article_content(self, article_url):
      response = requests.get(article_url)
      article_soup = BeautifulSoup(response.text, 'html.parser')

      # Find the main article tag
      article_tag = article_soup.find('article')

      # Initialize an empty list to hold all text pieces
      article_content = []

      if article_tag:
         # Extract text from all <p> tags and header tags within the article tag
         text_elements = article_tag.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
         for element in text_elements:
            text = element.get_text(strip=True)
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                  # Add formatting for headers
                  article_content.append(f"**{text}**\n")
            else:
                  # Add text with a newline for paragraphs
                  article_content.append(f"{text}\n")

      # Join all pieces of text into a single string
      full_article = ''.join(article_content)
      return full_article
   
   def get_tag(self):
      return self.tag

