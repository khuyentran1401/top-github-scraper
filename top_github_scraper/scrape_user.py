import json
import os
from pathlib import Path
from dotenv import load_dotenv
from rich import print
from top_github_scraper.utils import ScrapeGithubUrl, UserProfileGetter

load_dotenv()

USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")

def get_top_user_urls(
    keyword: str,
    save_directory: str=".",
    start_page: int = 1,
    stop_page: int = 50,
):
    """Get the URLs of the repositories pop up when searching for a specific
    keyword on GitHub.
    
    See PARAMETERs.md for a description of the parameters of this function
    """
    Path(save_directory).mkdir(parents=True, exist_ok=True)
    save_path = f"{save_directory}/top_repo_urls_{keyword}_{start_page}_{stop_page}.json"
    repo_urls = ScrapeGithubUrl(
        keyword, 'Users', 'followers', start_page, stop_page
    ).scrape_top_repo_url_multiple_pages()
    with open(save_path, "w") as outfile:
        json.dump(repo_urls, outfile)
    
def get_top_users(
    keyword: int,
    start_page: int = 1,
    stop_page: int = 50,
    save_directory: str="."
):
    """
    Get the information of the owners and contributors of the repositories pop up when searching for a specific
    keyword on GitHub.
    
    See PARAMETERs.md for a description of the parameters of this function.
    """
    safe_keyword = keyword.replace(" ","_")
    full_url_save_path = (
        f"{save_directory}/top_repo_urls_{safe_keyword}_{start_page}_{stop_page}.json"
    )
    user_save_path = f"{save_directory}/top_user_info_{safe_keyword}_{start_page}_{stop_page}.csv"
    if not Path(full_url_save_path).exists():
        get_top_user_urls(
            keyword=keyword,
            start_page=start_page,
            stop_page=stop_page,
            save_directory=save_directory,
        )
    with open(full_url_save_path, "r") as infile:
        user_urls = json.load(infile)
        url = 'https://api.github.com/users'
        urls = [url + user for user in user_urls]
        for i in range(len(urls)):
            # This is what the HTTP requet needs to be formatted: https://api.github.com/users/ZuzooVn
            # We need to remove the last part of the URL, after the final '/', to use the API correctly.
            index = urls[i].rfind('/')
            urls[i] = urls[i][:index]
        top_users = UserProfileGetter(urls).get_all_user_profiles()
        top_users.to_csv(user_save_path)
        return top_users