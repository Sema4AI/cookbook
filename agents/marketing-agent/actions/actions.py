"""
A bare-bone AI Action template

Please check out the base guidance on AI Actions in our main repository readme:
https://github.com/sema4ai/actions/blob/master/README.md

"""

from sema4ai.actions import action
import os
import time
import re
from helpers import TechCrunchScraper, MediumScraper
import json
from glob import glob
@action
def scrape_data_tc(tag: str, num_articles:int =10) -> bool:
    """
    Scrape TechCrunch articles based on a specific tag.
    
    Args:
        tag (str): The tag to search for.
        num_articles (int): The number of articles to scrape.
    
    Returns:
        bool: True if the action was successful, False otherwise.
    """
    scraper = TechCrunchScraper(tag)
    article_links = scraper.fetch_article_links(num_articles)
    dir_to_save = os.path.join(scraper.get_parent_dir(), scraper.get_tag().split('/')[-1])
    os.makedirs(dir_to_save, exist_ok=True)
    with open(os.path.join(dir_to_save, 'techcrunch_links.txt'), 'w+') as f:
        for link in article_links:
            f.write(link + '\n')
    for link in article_links:
        content = scraper.scrape_article_content(link)
        filename = os.path.join(dir_to_save, 'techcrunch-' + link.split('/')[-2] + '.txt')
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                print(f"Article already exists: {filename}")
                continue
            else:
                if content != '':
                    scraper.save_article_content(filename, content)
                    print(f"Article saved: {filename}")
                    scraper.save_title(filename, os.path.join(dir_to_save, 'titles.json'))
                    time.sleep(2)
                else:
                    print(f"Article not saved: {filename}, could not scrape content.")
                    continue   
        else:
            scraper.save_article_content(filename, content)
            print(f"Article saved: {filename}")
            scraper.save_title(filename, os.path.join(dir_to_save, 'titles.json'))
            time.sleep(2)
    return True

@action
def scrape_data_medium(tag: str, num_articles: int=10) -> bool:
    """
    Scrape articles from a Medium tag URL and save them to disk.
    
    Args:
        tag (str): Tag to scrape articles from
        num_articles (int): Number of articles to scrape
    
    Returns:
        bool: True if the action was successful, False otherwise
    """
    scraper = MediumScraper(tag)
    article_links = scraper.fetch_article_links(num_articles)
    dir_to_save = os.path.join(scraper.get_parent_dir(), scraper.get_tag().split('/')[-1])
    os.makedirs(dir_to_save, exist_ok=True)
    with open(os.path.join(dir_to_save, 'medium_links.txt'), 'w+') as f:
        for link in article_links:
            f.write(link + '\n')
    for link in article_links:
        content = scraper.scrape_article_content(link)
        # Create a simple filename from the article link
        # remove the number from the filename
        filename = os.path.join(dir_to_save, 'medium-' + link.split('/')[-1] + '.txt')
        if os.path.exists(filename):
            # member only story, can try to save it again
            if os.path.getsize(filename) > 0:
                print(f"Article already exists: {filename}")
                continue
            else:
                if content != '':
                    scraper.save_article_content(filename, content)
                    print(f"Article saved: {filename}")
                    scraper.save_title(filename, os.path.join(dir_to_save, 'titles.json'))
                    time.sleep(2)
                else:
                    print(f"Article not saved: {filename}, could not scrape content.")
                    continue   
            # print(f"Article already exists: {filename}")
            # continue
        else:
            scraper.save_article_content(filename, content)
            print(f"Article saved: {filename}")
            scraper.save_title(filename, os.path.join(dir_to_save, 'titles.json'))
            time.sleep(2)
    return True

@action
def load_json(tag: str, filename: str) -> str:
    """
    Load a JSON file.
    
    Args:
        tag (str): The tag to search for.
        filename (str): The filename of the JSON file to load.
    
    Returns:
        String represeeing the loaded JSON data.
    """
    parent_dir = "/tmp/tags"
    tag = tag.lower().replace(' ', '-')
    try:
        with open(os.path.join(parent_dir, tag, filename), 'r') as f:
            data = json.load(f)
        return str(data)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    except Exception as e:
        raise Exception(f"Error loading JSON file: {e}")
    
@action
def load_articles(tag: str) -> str:
    """
    Load all articles from a specific tag.
    
    Args:
        tag (str): The tag to search for.
    
    Returns:
        String representing the loaded articles.
    """
    parent_dir = "/tmp/tags"
    tag = tag.lower().replace(' ', '-')
    content = ''
    try:
        for filename in glob(os.path.join(parent_dir, tag, '*.txt')):
            with open(filename, 'r') as f:
                data = f.read()
                content += data + '\n-----------------\n'
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"No articles found for tag: {tag}")
    except Exception as e:
        raise Exception(f"Error loading articles: {e}")
            
        