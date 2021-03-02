import os 
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from rich import print 
from top_github_scraper.utils import ScrapeGithubUrl, UserProfileGetter      
import pandas as pd 

def test_keyword_to_url():
    res = ScrapeGithubUrl._keyword_to_url(page_num=1, keyword='machine learning', 
                        type="Users", sort_by='followers')

    assert res == "https://github.com/search?o=desc&p=1&q=machine+learning&s=followers&type=Users"

def test_scrape_top_repo_url_multiple_pages():
    res = ScrapeGithubUrl('machine learning', 'Repositories', 'stars', 1, 3).scrape_top_repo_url_multiple_pages()

def test_get_all_contributor_profiles():
    urls = ["https://api.github.com/users/jakevdp",
            "https://api.github.com/users/fuglede"]
    res = UserProfileGetter(urls).get_all_contributor_profiles()
    assert isinstance(res, pd.DataFrame)