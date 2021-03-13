from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
from rich.progress import track
from rich import print 
import pandas as pd 
import os
import warnings
from dotenv import load_dotenv
from typing import List
from IPython import get_ipython
from tqdm import tqdm
import logging


load_dotenv()
warnings.filterwarnings("ignore")

TYPES = ['Users', 'Repositories', 'Code', 'Commits', 'Issues', 'Packages', 'Topics']
SORT_BY = {'Users': ['followers'],
            'Repositories': ['', 'stars']}
SCRAPE_CLASS = {'Users': 'mr-1', 'Repositories': "v-align-middle"}

USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")

if USERNAME is None or TOKEN is None:
    logging.warning("""You are using Github API as an unauthenticated user. For unauthenticated requests, the rate limit allows for up to 60 requests per hour.
     Follow the instruction here to be authenticated and increase your rate limit: https://github.com/khuyentran1401/top-github-scraper#setup""")
class ScrapeGithubUrl:
    """Scrape top Github urls based on a certain keyword and type

    Parameters
    -------
    keyword: str
        keyword to search on Github
    type: str
        whether to search for User or Repositories
    sort_by: str 
        sort by best match or most stars, by default 'best_match', which will sort by best match. 
        Use 'stars' to sort by most stars.
    start_page_num: int
        page number to start scraping. The default is 0
    stop_page_num: int
        page number to stop scraping

    Returns
    -------
    List[str]
    """

    def __init__(self,keyword: str, type: str, sort_by: str, start_page_num: int, stop_page_num: int):
        self.keyword = keyword
        self.type = type
        self.start_page_num = start_page_num
        self.stop_page_num = stop_page_num
        if sort_by =='best_match':
            self.sort_by = ''
        else:
            self.sort_by = sort_by

    @staticmethod
    def _keyword_to_url(page_num: int, keyword: str, type: str, sort_by: str):
        """Change keyword to a url"""
        keyword_no_space = ("+").join(keyword.split(" "))
        return f"https://github.com/search?o=desc&p={str(page_num)}&q={keyword_no_space}&s={sort_by}&type={type}"

    def _scrape_top_repo_url_one_page(self, page_num: int):
        """Scrape urls of top Github repositories in 1 page"""
        url = self._keyword_to_url(page_num, self.keyword, type=self.type, sort_by=self.sort_by)
        page = requests.get(url)

        soup = BeautifulSoup(page.text, "html.parser")
        a_tags = soup.find_all("a", class_=SCRAPE_CLASS[self.type])
        urls = [a_tag.get("href") for a_tag in a_tags]

        return urls

    def scrape_top_repo_url_multiple_pages(self):
        """Scrape urls of top Github repositories in multiple pages"""
        urls = []
        if isnotebook():
            for page_num in tqdm(
                range(self.start_page_num, self.stop_page_num),
                desc="Scraping top GitHub URLs...",
            ):
                urls.extend(self._scrape_top_repo_url_one_page(page_num))
        else: 
            for page_num in track(
                range(self.start_page_num, self.stop_page_num),
                description="Scraping top GitHub URLs...",
            ):
                urls.extend(self._scrape_top_repo_url_one_page(page_num))

        return urls

class UserProfileGetter:
    """Get the information from users' homepage"""

    def __init__(self, urls: List[str]) -> pd.DataFrame:
        self.urls = urls
        self.profile_features = [
            "login",
            "url",
            "type",
            "name",
            "company",
            "location",
            "email",
            "hireable",
            "bio",
            "public_repos",
            "public_gists",
            "followers",
            "following",
        ]

    def _get_one_user_profile(self, profile_url: str):
        profile = requests.get(profile_url, auth=(USERNAME, TOKEN)).json()
        return {
            key: val
            for key, val in profile.items()
            if key in self.profile_features
        }

    def get_all_user_profiles(self):

        if isnotebook():
            all_contributors = [
            self._get_one_user_profile(url)
            for url in tqdm(
                self.urls, desc="Scraping top GitHub profiles..."
            )
        ]
        else:
            all_contributors = [
                self._get_one_user_profile(url)
                for url in track(
                    self.urls, description="Scraping top GitHub profiles..."
                )
            ]
        all_contributors_df = pd.DataFrame(all_contributors).reset_index(
            drop=True
        )

        return all_contributors_df


def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter