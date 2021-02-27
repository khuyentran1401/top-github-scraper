from top_github_scraper import scrape_github_url, scrape_repo, get_user_profile

if __name__=='__main__':
    keyword = "machine learning"
    stop_page = 1
    max_n_top_contributors = 2

    # scrape_github_url(keyword, stop_page=stop_page)
    # scrape_repo(keyword, stop_page=1, max_n_top_contributors=max_n_top_contributors)
    get_user_profile(keyword, max_n_top_contributors=max_n_top_contributors, stop_page=stop_page)