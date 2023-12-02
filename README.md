<div align="center">
<img src="images/PERCHAL.png" width="300px" alt="fuzzy">
</div>
<div>
<h1 align="center"><b>Web Scrapping Automator</b></h1>
</div>

# Perchal

Perchal is web scrapping automation tool to make the web-scrapping an easy job. Perchal automates the job of scraping web contents and mapping them into an CSV file for your need. Perchal takes care of locating and scraping web elements. All you need to do it ***configure*** PerChal using the ***config*** file to tune the scraping behaviour.

## Usage

```
Usage: perchal.py -c <config_file> -u <urllist_file> -o <output_filename>

Options:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config=CONFIG_FILE
                        Specify the path to the config file
  -u URL, --url-list=URL
                        Specify the path to the url list text file
  -o OUTFILE, --outfile=OUTFILE
                        Specify the output file name
```
  

## Requirements
1. Python 3
1. BeautifulSoup
2. JSON
3. OptParse

## Configurations

Perchal uses config files for locating and identifying the data from the web pages. Perchal accepts config file in a json format.

***The fields in the config file are explained as follows:***
1. **title** : This field is used for specifying the title of the CSV file field when generating the CSV file. Perchal works by allocating separate json objects for each data that you want to scrape from the web page.
2. **type** : This field is used for speciying the type of the web element. Is it dynamic or static. Static pages are pages where the structure of the DOM tree will be the same for all the urls in the url list. Dynamic contnts are web pages whose DOM tree structure won't be the same for all the urls in the url-list. By default, Perchal considers the static pages as dynamic pages. So the value in this is "**dynamic**"
3. **locator** : This field is used for specifying the locator or the static web element in the web page from where we can reach the original content that we need. Perchal accepts the locators both Strings and attributes. ***WHEN SPECIFYING THE ATTRIBUTES DON'T PUT THE TAG NAME. ONLY THE ATTRIBUTES OF THE TAG***. If the locator is a string, just give the exact string in the locator.
4. **identifier**: This field is used for specifying the information such as how to reach the original content to be scraped from the locator.
    1. **level** : This field is used for specifying the level of searching for Perchal, There are 2 levels of search hierarchy.
        1. **same** : specify same if the web element is located on the same hierarchy as the locator.
        2. **low** : specify low is the web element is located on the lower hierarchy than the locator. 
    2. **data** : This field is used for specifying the type of data. The type means how the scraper should scrape. In most cases, we might need to collect data from consecutive web elements. Sometimes we need to pick only the text from single element. In those cases, we can use this field for specification.
        1. **unique** : This value tells that the scraper should collect data from the single web element.
        2. **multiple** : This value tells that the scraper should collect data from the web element and the same consecutive web elements.
        3. **table** : This value tells that the scraper elemet is a table.
    3. **datatype** : This field is used for specying the type of the data whetehr it it string or link. specify **link** or **string**.
    4. **tag** : This value is used for specifying the tag name which hlolds the data to scraped.
    5. **parent** : This field should be given only if the **data** field is given as **table**. The value must be **tr**.
    6. **child** : This field should be given only if the **data** field is given as **table**. The value must be **td**.

## Methods
You can also import perchal as a module into your script and use its functionality. Perchal provides two methods for scraping.
1. **start_scraping_from_url** : provide the config file as json object and the url to fetch from. This will return the scraped contents from the web page as a list of lists
2. **start_scraping_from_text** : provide the config file as json object and the response body from the url which you have. This will return the scraped contents from the web page as a list of lists
