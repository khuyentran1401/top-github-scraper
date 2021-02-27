# Top Github Users Scraper

Scrape top Github repositories and users based on keywords.

![demo](https://github.com/khuyentran1401/top-github-scraper/blob/master/figures/demo.gif?raw=True)

## Installation
```bash
pip install top-github-scraper
```

## Usage
**Get Top Github Repositories' URLs**
```python
from top_github_scraper import get_top_urls

get_top_repos(keyword="machine learning", stop_page=20)
```
After running the script above, a file named 
* `top_repo_urls_<keyword>_<start_page>_<end_page>.json` 

will be saved to your current directory.

**Get Top Github Repositories' Information**
```python
from top_github_scraper import get_top_urls

get_top_urls("machine learning", stop_page=20)
```
After running the script above, 2 files named 
* `top_repo_urls_<keyword>_<start_page>_<end_page>.json` 
* `top_repo_info_<keyword>_<start_page>_<end_page>.json` 

will be saved to your current directory.

**Get Top Github Users' Profiles**
```python
from top_github_scraper import get_top_users

get_top_users("machine learning", stop_page=20)
```
After running the script above, 3 files named 
* `top_repo_urls_<keyword>_<start_page>_<end_page>.json` 
* `top_repo_info_<keyword>_<start_page>_<end_page>.json`
* `top_user_info_<keyword>_<start_page>_<end_page>.csv` 

will be saved to your current directory.

### Parameters
* **get_top_urls**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `save_path` : str, optional
        where to save the output file, by default `"top_repo_urls"`
    * `start_page` : int, optional
        page number to start scraping from, by default `0`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `50`
* **get_top_repos**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `max_n_top_contributors`: int
        number of top contributors in each repository to scrape from, by default `10`
    * `start_page` : int, optional
        page number to start scraping from, by default `0`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `50`
    * `url_save_path` : str, optional
        where to save the output file of URLs, by default `"top_repo_urls"`
    * `repo_save_path` : str, optional
        where to save the output file of repositories' information, by default `"top_repo_info"`
* **get_top_users**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `max_n_top_contributors`: int
        number of top contributors in each repository to scrape from, by default `10`
    * `start_page` : int, optional
        page number to start scraping from, by default `0`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `50`
    * `url_save_path` : str, optional
        where to save the output file of URLs, by default `"top_repo_urls"`
    * `repo_save_path` : str, optional
        where to save the output file of repositories' information, by default `"top_repo_info"`
    * `user_save_path` : str, optional
        where to save the output file of users' profiles, by default `"top_user_info"`
## How the Data is Scraped

`top-github-scraper` scrapes the owners as well as the contributors of the top repositories that pop up in the search when searching for a specific keyword on GitHub.

![image](https://github.com/khuyentran1401/top-github-scraper/blob/master/figures/machine_learning_results.png?raw=True)
For each user, `top-github-scraper` scrapes 16 data points:
* `login`: username
* `url`: URL of the user
* `contributions`: Number of contributions to the repository that the user is scraped from
* `stargazers_count`: Number of stars of the repository that the user is scraped from
* `forks_count`: Number of forks of the repository that the user is scraped from
* `type`: Whether this account is a user or an organization
* `name`: Name of the user
* `company`: User's company
* `location`: User's location
* `email`: User's email
* `hireable`: Whether the user is hireable
* `bio`: Short description of the user
* `public_repos`: Number of public repositories the user has (including forked repositories)
* `public_gists`: Number of public repositories the user has (including forked gists)
* `followers`: Number of followers the user has
* `following`: Number of people the user is following

