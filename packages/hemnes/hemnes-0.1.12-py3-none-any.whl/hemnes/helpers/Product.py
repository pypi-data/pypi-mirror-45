class Product:
    """Class to encapsulate stored product data.

    Attributes:
        name (str): name of the product
        id_no (str): product id
        price (float): price of the product
        url (str): url to the product page
        rating (float): customer rating of the product (None-able)
        img_urls (list[str]): urls to product images (None-able)
        colors (list[str]): colors associated with the product (None-able)
        tag (str): meta tag
    """

    def __init__(self, name, id_no, price, url, rating, img_urls, colors, tag=None):
        """Default Product constructor.

        The rating, img_urls, and colors fields are all None-able

        Args:
            name (str): name of the product
            id_no (str): product id
            price (float): price of the product
            url (str): url to the product page
            rating (float): user rating of the product
            img_urls (list[str]): urls to product images
            colors (list[str]): colors associated with the product
            tag (str): meta tag
        """
        self.name = name
        self.id_no = id_no
        self.price = price
        self.url = url
        self.rating = rating
        self.img_urls = img_urls
        self.colors = colors
        self.tag = tag
