from top_github_scraper import get_top_repo_urls, get_top_repos, get_top_contributors, get_top_user_urls, get_top_users

if __name__=='__main__':
    keyword = "machine learning"
    stop_page = 2
    max_n_top_contributors = 2
    sort_by = 'stars'
 
    # get_top_repo_urls("machine learning", stop_page=2)
    # get_top_repos(keyword="machine learning", stop_page=2)
    # get_top_contributors(keyword, stop_page=stop_page)

    get_top_users(keyword, stop_page=stop_page)