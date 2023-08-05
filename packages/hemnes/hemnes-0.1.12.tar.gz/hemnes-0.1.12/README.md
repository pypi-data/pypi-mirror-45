<!-- HEADER INFORMATION -->
<h3 align="center"><a href="https://pypi.org/project/hemnes/">HEMNES</a></h3>

<p align="center">
    <a href="https://github.com/sayeefrmoyen/hemnes/issues">Report Bug</a>
    ·
    <a href="https://github.com/sayeefrmoyen/hemnes/issues">Request Feature</a>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Requirements](#requirements)
  * [Installation](#install)
* [Usage](#usage)
* [What's Next](#problems)
* [Release History](#release-history)
* [License](#license)
* [Acknowledgments](#acknowledgments)

<!-- ABOUT THE PROJECT -->
## Updates

04/16 - repository code is currently out-of-sync as I do some major overhauls on the project. Installing from
pip should see no changes, and the information in the readme is all accurate and up-to-date. Just be aware that cloning
and trying to build from source will not work until further notice.

## About The Project

Hemnes is a simple python3 package for scraping data from Ikea. Hemnes supports multi-word & strict
queries, as well as saving data to json. The following data is scraped by Hemnes for each matching
product found:

* `name (str)`
* `price (float)`
* `rank (int)`: based on order that products are returned for the query
* `rating (float)`: average user rating
* `url (str)`: product url
* `color (list[str])`: list of colors as strings of the product
* `images (list[str])`: list of full urls to product images

### Built With
Powered by:
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [ChromeDriver](http://chromedriver.chromium.org/getting-started)
* [Selenium](https://www.seleniumhq.org)

<!-- GETTING STARTED -->
## Getting Started

### Requirements

Hemnes requires the following:

* chromedriver
* python3
* pip3

If you have Google Chrome then you should already have chromedriver installed. If not head to the [ChromeDriver](http://chromedriver.chromium.org/getting-started)
page and follow the install instructions. Make sure that chromedriver is on your system path in order for hemnes to work.

### Install

Hemnes is distributed as a pip package. It can be an installed using standard pip installation:
```sh
pip3 install hemnes
```

Import Hemnes into your python scripts:
```python
import hemnes
```

<!-- USAGE EXAMPLES -->
## Usage

Hemnes makes it easy to get detailed product data from Ikea

### Standard Use

For retrieving product results as a list to then process yourself simply call:
```python
product_results = hemnes.get_products("coffee table")
```

`product_results` will now contain a `list[Product]`

`Product` is a simple helper class which contains the following fields:

* `name (str)`
* `tag (str)`
* `price (float)`
* `rank (int)`: based on order that products are returned for the query
* `rating (float)`: average user rating
* `url (str)`: product url
* `color (list[str])`: list of colors as strings of the product
* `images (list[str])`: list of full urls to product images
	
`tag` is a meta-field that can be used flexibly. By default tag is set to `None`. Some example usages of tag may be:

* Keeping track of which batch each item was stored
* For use as a key in databases

### Saving results to JSON

If you would like to save the results to a json file you can add the `data_path` param:
```python
# saving results to json
product_results = hemnes.get_products("coffee table", data_path="data/coffeetable.json")
```

### Strict Keyword Searching

Hemnes supports "strict searching" to specify required descriptive keywords for returned results. To use this add a `keywords` param:
```python
# adding required keywords
product_results = hemnes.get_products("coffee table", keywords=["large", "wooden"])
```

Hemnes will look for the given keywords in each product's detailed description, and only return those products which contain
all of the given keywords.

### Using the meta Tag

To include a `tag` in the returned results simply pass it to the call:
```python
# including a tag
product_results = hemnes.get_products("coffee table", tag="tables")
```

### Enabling Logs

By default hemnes does not log any output messages. For queries that return many results, hemnes may take several or tens of minutes to complete. For such
queries (e.g. generic queries like "table", or other queries for popular products) seeing log messages can be helpful to know how far along you are.

Hemnes will log output regarding # of results found, # of pages, current page # being processed, current result # being processed, and skipped results
(if strict querying is enabled), in addition to any error messages in the event of a crash. (If you experience a crash it would be extremely helpful for you
to report the exact error message and method call that caused it on github)

To enable logs pass in the `log` param:
```python
# enabling logs
product_results = hemnes.get_products("coffee table", log=True")
```

### Changing Sleep Time

Ikea uses angular to generate many of its product pages. As a result, a `sleep_time` is defined when loading pages in order to
insure that the DOM is properly retrieved before trying to scrape the page. By default `sleep_time` is set to 4 seconds. Depending on
how fast your internet is, this may be too long or too short.

To alter the `sleep_time` for loading pages pass it as a parameter:
```python
# changing sleep time
product_results = hemnes.get_products("coffee table", sleep_time=4) # sleep_time must be an int
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- Known Problems -->
## Known Problems

* Chromedriver runs with GUI - this is to render DOM on Ikea's angular generated pages. If anyone knows a way around this please contact me

<!-- Release History -->
## Release History
Release History

* 0.1.11	
  	* Slight changes to logger class
* 0.1.10
	* Add logging
	* Add sleep time modification
	* Fix bug where chromedriver did not close after certain errors
	* Return partial results found before errors
* 0.1.1-0.1.1.9
	* Fix packaging bugs
* 0.1.0
	* First proper release
	* Documentation still **incomplete**
	* Price-based querying functionality implemented, but not yet made available

## Future

* Finish documentation
* Price-based querying functionality implemented, but not yet made available - do this

<!-- Acknowledgments -->
## Acknowledgments

* [Awesome README template](https://github.com/othneildrew/Best-README-Template/blob/master/README.md)