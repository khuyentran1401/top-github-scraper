import os
from top_github_scraper import get_top_repo_urls, get_top_repos, get_top_contributors, get_top_user_urls, get_top_users

"""
get_top_repo_urls - Returns the URLs of the top repos that show up when searched using the keyword and pages
get_top_repos - Gets the data for all the repos for all the pages searched through. Information are the github user names of each contributor.
get_top_contributors - returns all the contributors from all the pages that are searched through. 
get_top_user_urls - Gets the GitHub API URLs of the top users from the searched pages. Only 1 user from each repo is scraped.
get_top_users - returns the top user from each github repo that is found amongst all the pages searched.
"""

if __name__=='__main__':
    keyword = "machine learning"
    file_safe_keyword = keyword.replace(" ","_")
    start = 1
    stop = 2
    dir = f"./{file_safe_keyword}_{start}_{stop}"
    
    
    print(f"~~~~~ Starting to scrape GitHub repositories. ~~~~~")
    get_top_contributors(keyword=keyword, max_n_top_contributors=10, start_page=start,
                         stop_page=stop, get_user_info_only=True, save_directory=dir)
    
    get_top_users(keyword=keyword, start_page=start, stop_page=stop, save_directory=dir)
    
    num_pages = stop-start
    print(f"~~~~~ Done scraping {num_pages} page(s) of reposititories on GitHub when searching for {keyword}. ~~~~~")
    if dir:
        print(f"Results can be found in: {os.getcwd()}{dir.split('.')[-1]}")
    else:
        print(f"Results can be found in {os.getcwd()}")