# Web Scraper Action

A set of actions that you can use to scrape the TechCrunch and Medium websites to obtain articles which are present with a given tag.

- User/LLM provides a tag (such as "AI Agents"), and the number of articles they want to scrape as input,
- The actions scrape the article title, and their contents. Saves both to local storage. (Inside the `/tmp/` folder).
- The LLM can then use the content of these articles and their titles to draw insights and generate new content.
