# Top Github Users Scraper

Scrape top Github repositories and users based on keywords. 

I used this tool to analyze the top 1k machine learning users in [this article](https://towardsdatascience.com/i-scraped-more-than-1k-top-machine-learning-github-profiles-and-this-is-what-i-found-1ab4fb0c0474?sk=68156d6b1c05614d356645728fe02584).

![demo](https://github.com/khuyentran1401/top-github-scraper/blob/master/figures/demo.gif?raw=True)

## Setup

**Installation**
```bash
pip install top-github-scraper
```
**Add Credentials**

To make sure you can scrape many repositories and users, add your GitHub's credentials to `.env` file.
```bash
touch .env
```
Add your username and [token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) to `.env` file:
```bash
GITHUB_USERNAME=yourusername
GITHUB_TOKEN=yourtoken
```
## Usage
### Get Top Github Repositories' URLs
```python
from top_github_scraper import get_top_repo_urls

get_top_repo_urls(keyword="machine learning", stop_page=20)
```

Output at `top_repo_urls_<keyword>_<sort_by>_<start_page>_<end_page>.json`:
```python
[
    "/josephmisiti/awesome-machine-learning",
    "/wepe/MachineLearning",
    "/udacity/machine-learning",
    "/Jack-Cherish/Machine-Learning",
    "/ZuzooVn/machine-learning-for-software-engineers",
    "/rasbt/python-machine-learning-book",
    "/lawlite19/MachineLearning_Python",
    "/lazyprogrammer/machine_learning_examples",
    "/trekhleb/homemade-machine-learning",
    "/ujjwalkarn/Machine-Learning-Tutorials"
]
```

### Get Top Github Repositories' Information
```python
from top_github_scraper import get_top_repos

get_top_repos("machine learning", stop_page=20)
```
Output for 1 repository at `top_repo_info_<keyword>_<sort_by>_<start_page>_<end_page>.json` :
```python
{
        "stargazers_count": 48620,
        "forks_count": 12155,
        "contributors": {
            "login": [
                "josephmisiti",
                "josephmmisiti",
                "hslatman",
                "0asa",
                "ajkl",
                "ipcenas",
                "cogmission",
                "spekulatius",
                "basickarl",
                "NathanEpstein"
            ],
            "url": [
                "https://api.github.com/users/josephmisiti",
                "https://api.github.com/users/josephmmisiti",
                "https://api.github.com/users/hslatman",
                "https://api.github.com/users/0asa",
                "https://api.github.com/users/ajkl",
                "https://api.github.com/users/ipcenas",
                "https://api.github.com/users/cogmission",
                "https://api.github.com/users/spekulatius",
                "https://api.github.com/users/basickarl",
                "https://api.github.com/users/NathanEpstein"
            ],
            "contributions": [
                671,
                105,
                21,
                12,
                11,
                9,
                8,
                7,
                7,
                7
            ]
        }
    }
```

### Get Top Github Contributors' Profiles
```python
from top_github_scraper import get_top_contributors

get_top_contributors("machine learning", stop_page=20)
```
Output at `top_contributor_info_<keyword>_<sort_by>_<start_page>_<end_page>.csv`:

|| login | url | type | name | company | location | email | hireable | bio | public_repos | public_gists | followers |following
| ------------- |:-------------:|:-------------:| :-----:| :-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
| 0 | josephmisiti | https://api.github.com/users/josephmisiti | User | Joseph Misiti | Math & Pencil |"Brooklyn, NY"|  | True | Mathematician & Co-founder of Math & Pencil|229|142|2705|275
1|josephmmisiti|https://api.github.com/users/josephmmisiti|User|||||||0|0|2|0
2|hslatman|https://api.github.com/users/hslatman|User|Herman Slatman|DistributIT|||||133|20|469|67
3|0asa|https://api.github.com/users/0asa|User|Vincent Botta| | Belgium|||"Innovation Engineer @evs-broadcast, previously Data Scientist @kensuio, E-Marketing Tools Manager @Diagenode, cofounder @Antibody-Adviser and photographer"|35|15|25|16
4|ajkl|https://api.github.com/users/ajkl|User|Ajinkya Kale|||kaleajinkya@gmail.com|||58|1|29|4
5|ipcenas|https://api.github.com/users/ipcenas|User|||||||79|0|1|0
6|cogmission|https://api.github.com/users/cogmission|User|David Ray||Third planet from the sun...|cognitionmission@gmail.com||Humanity's freedom and abundance through the pursuit of technological innovation in the area of cognitive applications - Cognition Mission|30|19|54|44
7|spekulatius|https://api.github.com/users/spekulatius|User|Peter Thaleikis|@bringyourownideas |127.0.0.1||True|Software engineer focused on solutions using open source and simply filling in the gaps to fulfill the requirements.|42|1|232|920
8|basickarl|https://api.github.com/users/basickarl|User|Karl Morrison||"Malmö, Sweden"|karl@basickarl.io||The question is: Will you take me seriously|5|1|12|6
9|NathanEpstein|https://api.github.com/users/NathanEpstein|User|Nathan Epstein||"New York, NY"|nathanepst@gmail.com|True||23|12|208|0

### Get Top Github Users' Profiles
```python
from top_github_scraper import get_top_users

get_top_users("machine learning", stop_page=20)
```
Output at `top_user_info_<keyword>_<start_page>_<end_page>.csv`

|| login | url | type | name | company | location | email | hireable | bio | public_repos | public_gists | followers |following
| ------------- |:-------------:|:-------------:| :-----:| :-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
0|rasbt|https://api.github.com/users/rasbt|User|Sebastian Raschka|UW-Madison|"Madison, WI"|||"Machine Learning researcher & open source contributor. Author of ""Python Machine Learning."" Asst. Prof. of Statistics @ UW-Madison."|71|5|13888|35
1|tqchen|https://api.github.com/users/tqchen|User|Tianqi Chen|"CMU, OctoML"||||Large scale Machine Learning|28|1|8611|126
2|halfrost|https://api.github.com/users/halfrost|User|halfrost|@Alibaba | Shanghai China|i@halfrost.com||💪天道酬勤，勤能补拙。博观而约取，厚积而薄发。Gopher / Rustacean / iOS Dev. / Machine Learning / Retired acmer / Math / Philosophy / Technical Writer.|22|0|8566|314
3|ageron|https://api.github.com/users/ageron|User|Aurélien Geron||Paris|||Author of the book Hands-On Machine Learning with Scikit-Learn and TensorFlow. Former PM of YouTube video classification and founder & CTO of a telco operator.|43|16|8383|2
4|chiphuyen|https://api.github.com/users/chiphuyen|User|Chip Huyen|https://snorkel.ai|"Mountain View, CA"||True|Developing tools and best practices for machine learning production.|19|1|7839|15
5|rhiever|https://api.github.com/users/rhiever|User|Randy Olson|FOXO BioScience|"Vancouver, WA"|rso@randalolson.com||"Chief Data Scientist, @FOXOBioScience. AI, Machine Learning, and Data Visualization specialist. Community leader for /r/DataIsBeautiful."|77|17|5363|13
6|lexfridman|https://api.github.com/users/lexfridman|User|Lex Fridman|MIT|"Cambridge, MA"|||"AI researcher working on autonomous vehicles, human-robot interaction, and machine learning at MIT and beyond."|2|0|5031|0
7|eriklindernoren|https://api.github.com/users/eriklindernoren|User|Erik Linder-Norén||"Stockholm, Sweden"|eriklindernoren@gmail.com||"ML engineer at Apple. Excited about machine learning, basketball and building things."|24|0|3764|11
8|roboticcam|https://api.github.com/users/roboticcam|User|A/Prof Richard Xu                 徐亦达教授|University of Technology Sydney|Sydney Australia|||"I am an A/Professor in Machine Learning at UTS. manage a large research team of postdoc, PhD students close to 30 people"|10|0|3561|0
9|ogrisel|https://api.github.com/users/ogrisel|User|Olivier Grisel|Inria|"Paris, France"|olivier.grisel@ensta.org||Machine Learning Engineer a Inria Saclay (Parietal team).|174|93|3237|116

### Parameters

* **get_top_urls**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `sort_by`: str 
        sort by best match or most stars, by default `''`, which will sort by best match. 
        Use `'stars'` to sort by most stars.
    * `save_path` : str, optional
        where to save the output file, by default `"top_repo_urls"`
    * `start_page` : int, optional
        page number to start scraping from, by default `1`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `50`
* **get_top_repos**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `sort_by`: str 
        sort by best match or most stars, by default `''`, which will sort by best match. 
        Use `'stars'` to sort by most stars.
    * `max_n_top_contributors`: int
        number of top contributors in each repository to scrape from, by default `10`
    * `start_page` : int, optional
        page number to start scraping from, by default `1`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `50`
    * `url_save_path` : str, optional
        where to save the output file of URLs, by default `"top_repo_urls"`
    * `repo_save_path` : str, optional
        where to save the output file of repositories' information, by default `"top_repo_info"`
* **get_top_users**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `sort_by`: str 
        sort by best match or most stars, by default '', which will sort by best match. 
        Use 'stars' to sort by most stars.
    * `max_n_top_contributors`: int
        number of top contributors in each repository to scrape from, by default `10`
    * `start_page` : int, optional
        page number to start scraping from, by default `1`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `50`
    * `url_save_path` : str, optional
        where to save the output file of URLs, by default `"top_repo_urls"`
    * `repo_save_path` : str, optional
        where to save the output file of repositories' information, by default `"top_repo_info"`
    * `user_save_path` : str, optional
        where to save the output file of users' profiles, by default `"top_contributor_info"`
* **get_top_user_urls**
    * `keyword` : str
        Keyword to search for (.i.e, machine learning)
    * `save_path` : str, optional
        where to save the output file, by default `"top_repo_urls"`
    * `start_page` : int, optional
        page number to start scraping from, by default `1`
    * `stop_page` : int, optional
        page number of the last page to scrape, by default `50`
## How the Data is Scraped

`top-github-scraper` scrapes the owners as well as the contributors of the top repositories that pop up in the search when searching for a specific keyword on GitHub.

![image](https://github.com/khuyentran1401/top-github-scraper/blob/master/figures/machine_learning_results.png?raw=True)

For each user, `top-github-scraper` scrapes 16 data points:
* `login`: username
* `url`: URL of the user
* `contributions`: Number of contributions to the repository that the user is scraped from
* `stargazers_count`: Number of stars of the repository that the user is scraped from
* `forks_count`: Number of forks of the repository that the user is scraped from
* `type`: Whether this account is a user or an organization
* `name`: Name of the user
* `company`: User's company
* `location`: User's location
* `email`: User's email
* `hireable`: Whether the user is hireable
* `bio`: Short description of the user
* `public_repos`: Number of public repositories the user has (including forked repositories)
* `public_gists`: Number of public repositories the user has (including forked gists)
* `followers`: Number of followers the user has
* `following`: Number of people the user is following

