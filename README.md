# Installation instructions on Ubuntu 16.04

Install and create a new virtual environment

`sudo apt install python3-venv`

`python3 -m venv scraper`

`source scraper/bin/activate`

Install dependencies for scrapy

`sudo apt install python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev`

Clone repo

`git clone https://github.com/ploggingdev/scrape_github`

`cd scrape_github`

Install dependencies. **Note**: Atleast 1GB RAM is required. `lxml` will fail to install with less than 1GB RAM.

`pip install -r requirements.txt`

Add environment variable.

`nano ~/.bashrc`

To get your access token, refer [here](https://developer.github.com/v3/oauth/).

Append the following at the end of your `.bashrc`

`export github_token="YOUR_TOKEN"`

`source ~/.bashrc`

`cd github_scraper`

Run scrapy in the background to get repos

`nohup scrapy crawl github -o all_repos.jsonl -t jsonlines &`

`cd ../`

Get language details of repos. This is also run in the background.

`nohup python language_scraper.py &`

Run the script and choose what graph should be displayed

`python generate_bar_chart.py`
