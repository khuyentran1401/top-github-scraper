from top_github_scraper import get_top_urls, get_top_repos, get_top_users

if __name__=='__main__':
    keyword = "machine learning"
    stop_page = 1
    max_n_top_contributors = 2

    # get_top_urls(keyword, stop_page=stop_page)
    get_top_repos(keyword, stop_page=1, max_n_top_contributors=max_n_top_contributors)
    # get_top_users(keyword, max_n_top_contributors=max_n_top_contributors, stop_page=stop_page)