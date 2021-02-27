import os
import warnings
from dataclasses import dataclass
from typing import List

import requests

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path
from rich import print
import json 
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore")

USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")


@dataclass
class ScrapeGithubUrl:
    """Scrape top Github Repos urls based on a certain keyword

    Returns
    -------
    keyword: str
        keyword to search on Github
    start_page_num: int
        page number to start scraping. The default is 0
    stop_page_num: int
        page number to stop scraping
    """

    keyword: str
    start_page_num: int
    stop_page_num: int

    @staticmethod
    def _keyword_to_url(page_num: int, keyword: str):
        """Change keyword to a url"""
        keyword_no_space = ("+").join(keyword.split(" "))
        return f"https://github.com/search?o=desc&p={str(page_num)}&q={keyword_no_space}&s=&type=Repositories"

    def _scrape_top_repo_url_one_page(self, page_num: int):
        """Scrape urls of top Github repositories in 1 page"""
        url = self._keyword_to_url(page_num, self.keyword)
        page = requests.get(url)

        soup = BeautifulSoup(page.text, "html.parser")
        a_tags = soup.find_all("a", class_="v-align-middle")
        urls = [a_tag.get("href") for a_tag in a_tags]
        return urls

    def scrape_top_repo_url_multiple_pages(self):
        """Scrape urls of top Github repositories in multiple pages"""
        urls = []
        for page_num in tqdm(range(self.start_page_num, self.stop_page_num)):
            urls.extend(self._scrape_top_repo_url_one_page(page_num))

        return urls


class RepoScraper:
    """Scrape information of repos and the
    contributors of those repositories"""

    def __init__(self, repo_urls: list, max_n_top_contributors: int):
        self.repo_urls = repo_urls
        self.max_n_top_contributors = max_n_top_contributors

    def get_all_top_repo_information(self):
        top_repo_infos = []
        for repo_url in tqdm(self.repo_urls):
            top_repo_infos.append(self._get_repo_information(repo_url))


        return top_repo_infos

    def _get_repo_information(self, repo_url: str):
        repo_info_url = f"https://api.github.com/repos{repo_url}"
        repo_info = requests.get(repo_info_url, auth=(USERNAME, TOKEN)).json()

        info_to_scrape = ["stargazers_count", "forks_count"]
        repo_important_info = {}
        for info in info_to_scrape:
            repo_important_info[info] = repo_info[info]

        repo_important_info["contributors"] = self._get_contributor_repo_of_one_repo(
            repo_url
        )

        return repo_important_info

    def _get_contributor_repo_of_one_repo(self, repo_url: str):

        # https://api.github.com/repos/josephmisiti/awesome-machine-learning/contributors
        contributor_url = f"https://api.github.com/repos{repo_url}/contributors"
        contributor_page = requests.get(contributor_url, auth=(USERNAME, TOKEN)).json()

        contributors_info = {"login": [], "url": [], "contributions": []}

        max_n_top_contributors = self._find_max_n_top_contributors(
            num_contributors=len(contributor_page)
        )
        n_top_contributor = 0

        while n_top_contributor < max_n_top_contributors:
            contributor = contributor_page[n_top_contributor]

            self._get_contributor_general_info(contributors_info, contributor)
            n_top_contributor += 1

        return contributors_info

    @staticmethod
    def _get_contributor_general_info(contributors_info: List[dict], contributor: dict):

        contributors_info["login"].append(contributor["login"])
        contributors_info["url"].append(contributor["url"])
        contributors_info["contributions"].append(contributor["contributions"])

    def _find_max_n_top_contributors(self, num_contributors: int):
        if num_contributors > self.max_n_top_contributors:
            return self.max_n_top_contributors
        else:
            return num_contributors


class DataProcessor:
    def __init__(self, data: list):
        self.data = data

    def process(self) -> pd.DataFrame:

        repos = [self.process_one_repo(repo) for repo in self.data]
        return pd.concat(repos).reset_index(drop=True)

    def process_one_repo(self, repo_info: dict):
        contributors_info = repo_info["contributors"]
        contributors_info = pd.DataFrame(contributors_info)

        repo_stats = self.get_repo_stats(repo_info)

        for col_name, val in repo_stats.items():
            contributors_info[col_name] = val

        return contributors_info

    @staticmethod
    def get_repo_stats(repo_info: dict):
        repo_stats_list = [
            "stargazers_count",
            "forks_count",
            "created_at",
            "updated_at",
        ]
        return {key: val for key, val in repo_info.items() if key in repo_stats_list}


class UserProfileGetter:
    """Get the information from users' homepage"""

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.profile_features = [
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

    def _get_one_contributor_profile(self, profile_url: str):
        profile = requests.get(profile_url, auth=(USERNAME, TOKEN)).json()
        return {
            key: val for key, val in profile.items() if key in self.profile_features
        }

    def get_all_contributor_profiles(self):

        all_contributors = [
            self._get_one_contributor_profile(url) for url in tqdm(self.data["url"])
        ]
        all_contributors_df = pd.DataFrame(all_contributors).reset_index(drop=True)

        return pd.concat([self.data, all_contributors_df], axis=1)

def scrape_github_url(keyword: str, save_path: str='top_repo_urls', start_page: int=0, stop_page: int=50):
    save_path += f"_{keyword}_{start_page}_{stop_page}.json"
    repo_urls =  ScrapeGithubUrl(keyword, start_page, stop_page).scrape_top_repo_url_multiple_pages()
    with open(save_path, 'w') as outfile:
        json.dump(repo_urls, outfile)

def scrape_repo(keyword: int, max_n_top_contributors: int=10,  start_page:int=0, stop_page:int=50, 
                url_save_path: str="top_repo_urls", repo_save_path: str="top_repo_info"):
    full_url_save_path = f"{url_save_path}_{keyword}_{start_page}_{stop_page}.json"
    repo_save_path += f"_{keyword}_{start_page}_{stop_page}.json"

    if not Path(full_url_save_path).exists():
        scrape_github_url(keyword, url_save_path, start_page, stop_page)
    with open(full_url_save_path, 'r') as infile:
        repo_urls = json.load(infile)
        top_repos =  RepoScraper(repo_urls, max_n_top_contributors).get_all_top_repo_information()
        with open(repo_save_path, 'w') as outfile:
            json.dump(top_repos, outfile)

def get_user_profile(keyword: int, max_n_top_contributors: int=10,  start_page:int=0, stop_page:int=50, 
                    url_save_path: str="top_repo_urls", repo_save_path: str="top_repo_info",
                    user_save_path: str="top_user_info"):
    full_repo_save_path = f"{repo_save_path}_{keyword}_{start_page}_{stop_page}.json"
    user_save_path += f"_{keyword}_{start_page}_{stop_page}.csv"
    if not Path(full_repo_save_path).exists():
        scrape_repo(keyword, max_n_top_contributors, start_page, stop_page, url_save_path, repo_save_path)
    with open(full_repo_save_path, "r") as infile:
        repo_info = json.load(infile)
        repo_info = DataProcessor(repo_info).process()
        top_users = UserProfileGetter(repo_info).get_all_contributor_profiles()
        print(top_users)
        top_users.to_csv(user_save_path)
        

