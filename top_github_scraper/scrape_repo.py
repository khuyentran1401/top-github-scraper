import json
import os
from pathlib import Path
from typing import List

import pandas as pd
import requests
from dotenv import load_dotenv
from rich import print
from rich.progress import track
from tqdm import tqdm
from top_github_scraper.utils import ScrapeGithubUrl, UserProfileGetter, isnotebook
import logging

load_dotenv()

USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")

class RepoScraper:
    """Scrape information of repos and the
    contributors of those repositories"""

    def __init__(self, repo_urls: list, max_n_top_contributors: int):
        self.repo_urls = repo_urls
        self.max_n_top_contributors = max_n_top_contributors

    def get_all_top_repo_information(self):
        top_repo_infos = []

        if isnotebook():
            for repo_url in tqdm(
            self.repo_urls, desc="Scraping top GitHub repositories..."
            ):
                top_repo_infos.append(self._get_repo_information(repo_url))
        else:
            for repo_url in track(
                self.repo_urls, description="Scraping top GitHub repositories..."
            ):
                top_repo_infos.append(self._get_repo_information(repo_url))

        return top_repo_infos

    def _get_repo_information(self, repo_url: str):
        repo_info_url = f"https://api.github.com/repos{repo_url}"
        repo_info = requests.get(repo_info_url, auth=(USERNAME, TOKEN)).json()
        info_to_scrape = ["stargazers_count", "forks_count"]
        repo_important_info = {}
        for info in info_to_scrape:
            repo_important_info[info] = repo_info[info]

        repo_important_info[
            "contributors"
        ] = self._get_contributor_repo_of_one_repo(repo_url)

        return repo_important_info

    def _get_contributor_repo_of_one_repo(self, repo_url: str):

        # https://api.github.com/repos/josephmisiti/awesome-machine-learning/contributors
        contributor_url = (
            f"https://api.github.com/repos{repo_url}/contributors"
        )
        contributor_page = requests.get(
            contributor_url, auth=(USERNAME, TOKEN)
        ).json()

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
    def _get_contributor_general_info(
        contributors_info: List[dict], contributor: dict
    ):

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
        return {
            key: val
            for key, val in repo_info.items()
            if key in repo_stats_list
        }


def get_top_repo_urls(
    keyword: str,
    sort_by: str='best_match', 
    save_directory: str=".",
    start_page: int = 1,
    stop_page: int = 10,
):
    """Get the URLs of the repositories pop up when searching for a specific
    keyword on GitHub.

    Parameters
    ----------
    keyword : str
        Keyword to search for (.i.e, machine learning)
    sort_by: str 
        sort by best match or most stars, by default 'best_match', which will sort by best match. 
        Use 'stars' to sort by most stars.
    save_directory: str, optional 
        directory to save the output file, by default "."
    start_page : int, optional
        page number to start scraping from, by default 1
    stop_page : int, optional
        page number of the last page to scrape, by default 10
    """
    try: 
        Path(save_directory).mkdir(parents=True, exist_ok=True)
        full_path = f'{save_directory}/top_repo_urls_{keyword}_{sort_by}_{start_page}_{stop_page}.json'
        repo_urls = ScrapeGithubUrl(
            keyword, 'Repositories', sort_by, start_page, stop_page
        ).scrape_top_repo_url_multiple_pages()

        with open(full_path, "w") as outfile:
            json.dump(repo_urls, outfile)
        return repo_urls
    except Exception as e:
        print(e)
        logging.error("""You might ran out of rate limit. Are you an authenticated user? If you ran out of rate limit while requesting as an authenticated user, 
        either decrease the number of pages to scrape or to wait until more requests are available.""")


def get_top_repos(
    keyword: int,
    sort_by: str='best_match',
    save_directory: str=".",
    max_n_top_contributors: int = 10,
    start_page: int = 1,
    stop_page: int = 10,
):
    """Get the information of the repositories pop up when searching for a specific
    keyword on GitHub.

    Parameters
    ----------
    keyword : str
        Keyword to search for (.i.e, machine learning)
    sort_by: str 
        sort by best match or most stars, by default 'best_match', which will sort by best match. 
        Use 'stars' to sort by most stars.
    max_n_top_contributors: int
        number of top contributors in each repository to scrape from, by default 10
    start_page : int, optional
        page number to start scraping from, by default 1
    stop_page : int, optional
        page number of the last page to scrape, by default 10
    save_directory: str, optional 
        directory to save the output file, by default "."
    """
    try:
        full_url_save_path = (
            f"{save_directory}/top_repo_urls_{keyword}_{sort_by}_{start_page}_{stop_page}.json"
        )
        repo_save_path = f"{save_directory}/top_repo_info_{keyword}_{sort_by}_{start_page}_{stop_page}.json"

        if not Path(full_url_save_path).exists():
            get_top_repo_urls(keyword=keyword, sort_by=sort_by, save_directory=save_directory, start_page=start_page, stop_page=stop_page)
        with open(full_url_save_path, "r") as infile:
            repo_urls = json.load(infile)
            top_repos = RepoScraper(
                repo_urls, max_n_top_contributors
            ).get_all_top_repo_information()

        with open(repo_save_path, "w") as outfile:
            json.dump(top_repos, outfile)
        return top_repos

    except Exception as e:  
        print(e)
        logging.error("""You might ran out of rate limit. Are you an authenticated user? If you ran out of rate limit while requesting as an authenticated user, 
        either decrease the number of pages to scrape or to wait until more requests are available.""")

def get_top_contributors(
    keyword: int,
    sort_by: str='best_match', 
    max_n_top_contributors: int = 10,
    start_page: int = 1,
    stop_page: int = 10,
    get_user_info_only: bool=True, 
    save_directory: str=".",
):
    """
    Get the information of the owners and contributors of the repositories pop up when searching for a specific
    keyword on GitHub.
    Parameters
    ----------
    keyword : str
        Keyword to search for (.i.e, machine learning)
    sort_by: str 
        sort by best match or most stars, by default 'best_match', which will sort by best match. 
        Use 'stars' to sort by most stars.
    max_n_top_contributors: int
        number of top contributors in each repository to scrape from, by default 10
    start_page : int, optional
        page number to start scraping from, by default 1
    stop_page : int, optional
        page number of the last page to scrape, by default 10
    get_user_info_only: bool, optional
        whether to get the information of only contributors or to get the information of both contributors 
        and repositories contributors were scraped from, by default True, which means to get only contributors' information
    save_directory: str, optional 
        directory to save the output file, by default "."
    url_save_path : str, optional
        where to save the output file of URLs, by default "top_repo_urls"
    repo_save_path : str, optional
        where to save the output file of repositories' information, by default "top_repo_info"
    user_save_path : str, optional
        where to save the output file of users' profiles, by default "top_contributor_info"
    """

    full_repo_save_path = (
        f"{save_directory}/top_repo_info_{keyword}_{sort_by}_{start_page}_{stop_page}.json"
    )
    user_save_path = f"{save_directory}/top_contributor_info_{keyword}_{sort_by}_{start_page}_{stop_page}.csv"
    if not Path(full_repo_save_path).exists():
        get_top_repos(
            keyword=keyword,
            sort_by=sort_by,
            max_n_top_contributors=max_n_top_contributors,
            start_page=start_page,
            stop_page=stop_page,
            save_directory=save_directory
        )
    with open(full_repo_save_path, "r") as infile:
        repo_info = json.load(infile)
        repo_info = DataProcessor(repo_info).process()
        urls = repo_info['url']
        top_users = UserProfileGetter(urls).get_all_user_profiles()
        if get_user_info_only:
            top_users.to_csv(user_save_path)
            return top_users
        else:
            repo_and_top_users = pd.concat([repo_info, top_users], axis=1)
            repo_and_top_users = repo_and_top_users.loc[:,~repo_and_top_users.columns.duplicated()]
            repo_and_top_users.to_csv(user_save_path)
            return repo_and_top_users
