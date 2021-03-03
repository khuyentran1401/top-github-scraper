import json
import os
import warnings
from pathlib import Path

from dotenv import load_dotenv
from rich import print
from top_github_scraper.utils import ScrapeGithubUrl, UserProfileGetter


load_dotenv()
warnings.filterwarnings("ignore")

USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")

def get_top_user_urls(
    keyword: str,
    save_path: str = "top_user_urls",
    start_page: int = 1,
    stop_page: int = 50,
):
    """Get the URLs of the repositories pop up when searching for a specific
    keyword on GitHub.

    Parameters
    ----------
    keyword : str
        Keyword to search for (.i.e, machine learning)
    save_path : str, optional
        where to save the output file, by default "top_repo_urls"
    start_page : int, optional
        page number to start scraping from, by default 1
    stop_page : int, optional
        page number of the last page to scrape, by default 50
    """
    save_path += f"_{keyword}_{start_page}_{stop_page}.json"
    repo_urls = ScrapeGithubUrl(
        keyword, 'Users', 'followers', start_page, stop_page
    ).scrape_top_repo_url_multiple_pages()
    with open(save_path, "w") as outfile:
        json.dump(repo_urls, outfile)
    
def get_top_users(
    keyword: int,
    start_page: int = 1,
    stop_page: int = 50,
    url_save_path: str = "top_user_urls",
    user_save_path: str = "top_user_info",
):
    """
    Get the information of the owners and contributors of the repositories pop up when searching for a specific
    keyword on GitHub.
    Parameters
    ----------
    keyword : str
        Keyword to search for (.i.e, machine learning)
    start_page : int, optional
        page number to start scraping from, by default 1
    stop_page : int, optional
        page number of the last page to scrape, by default 50
    url_save_path : str, optional
        where to save the output file of URLs, by default "top_repo_urls"
    user_save_path : str, optional
        where to save the output file of users' profiles, by default "top_user_info"
    """
    full_url_save_path = (
        f"{url_save_path}_{keyword}_{start_page}_{stop_page}.json"
    )
    user_save_path += f"_{keyword}_{start_page}_{stop_page}.csv"
    if not Path(full_url_save_path).exists():
        get_top_user_urls(
            keyword=keyword,
            start_page=start_page,
            stop_page=stop_page,
            save_path=url_save_path,
        )
    with open(full_url_save_path, "r") as infile:
        user_urls = json.load(infile)
        url = 'https://api.github.com/users'
        urls = [url + user for user in user_urls]
        top_users = UserProfileGetter(urls).get_all_user_profiles()
        top_users.to_csv(user_save_path)
        return top_users