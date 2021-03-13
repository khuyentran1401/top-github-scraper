### Parameters

* **get_top_urls**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `sort_by`: str 
        sort by best match or most stars, by default `'best_match'`, which will sort by best match. 
        Use `'stars'` to sort by most stars.
    * `save_directory`: str, optional 
        directory to save the output file, by default `"."`
    * `start_page` : int, optional
        page number to start scraping from, by default `1`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `10`
* **get_top_repos**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `sort_by`: str 
        sort by best match or most stars, by default `'best_match'`, which will sort by best match. 
        Use `'stars'` to sort by most stars.
    * `max_n_top_contributors`: int
        number of top contributors in each repository to scrape from, by default `10`
    * `start_page` : int, optional
        page number to start scraping from, by default `1`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `10`
    * `save_directory`: str, optional 
        directory to save the output file, by default `"."`
* **get_top_contributors**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `sort_by`: str 
        sort by best match or most stars, by default `'best_match'`, which will sort by best match. 
        Use `'stars'` to sort by most stars.
    * `max_n_top_contributors`: int
        number of top contributors in each repository to scrape from, by default `10`
    * `start_page` : int, optional
        page number to start scraping from, by default `1`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `10`
    * `get_user_info_only`: bool, optional
        whether to get the information of only contributors or to get the information of both contributors 
        and repositories contributors were scraped from, by default `True`, which means to get only contributors' information
    * `save_directory`: str, optional 
        directory to save the output file, by default `"."`
* **get_top_users**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `start_page` : int, optional
        page number to start scraping from, by default `1`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `10`
    * `save_directory`: str, optional 
        directory to save the output file, by default `"."`
* **get_top_user_urls**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `save_directory`: str, optional 
        directory to save the output file, by default `"."`
    * `start_page` : int, optional
        page number to start scraping from, by default `1`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `10`