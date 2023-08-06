"""Main functionality for hemnes - ikea scraping"""

__author__ = 'sayeef moyen'

# import
from hemnes.helpers import Logger, Options, PageFetcher, Product, scrape
import json

def process_query(query, options=None):
    """Returns a list of products found for a query.

    Args:
        query (str): query words
        options (Options): Options object specifying extended requirements/actions

    Returns:
        list[Product]: Products found
    """
    ext_options = Options.Options() if options is None else options
    pf = PageFetcher.PageFetcher(chromedriver_path=ext_options.cdriver_path, sleep_time=ext_options.sleep_time)
    logger = None if not ext_options.log else Logger.Logger()
    # pass in the options
    results = scrape.process_query(pf, query, keywords=ext_options.keywords, logger=logger, num_desired=ext_options.num_results, strict=ext_options.strict, tag=ext_options.tag)
    pf.close()
    if logger is not None: logger.close()
    # writing to json if requested
    if ext_options.json_dump is not None:
        # turn all of the Product objects into dictionaries before writing to json
        json_friendly_results = [product.to_dict() for product in results]
        with open(ext_options.json_dump, 'w+') as json_dump:
            json.dump(json_friendly_results, json_dump, indent=4)
    return results
