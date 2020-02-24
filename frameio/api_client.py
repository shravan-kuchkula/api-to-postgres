class APIClient:
    """
    A class used to represent API Client

    Attributes
    ----------
    url : str
        an api url string that can be used to make a get request
    headers: dict
        a dictionary of request headers. Ex: Authentication header
    session: requests.Session
        a session object to make get requests

    Methods
    -------
    get_pages()
        handles paginated results by sending results one page at a time
    """
    def __init__(self,
                 url,
                 headers,
                 session):
        # map the params
        self.url = url
        self.headers = headers
        self.session = session

    def get_pages(self):
        """
        Handles paginated results by sending results one page at a time

        Raises
        ------
        HTTPError
            If there is any issue connecting to the API

        Returns
        -------
        page
            Returns a generator containing page results
        """
        response = self.session.get(self.url, headers=self.headers)
        response.raise_for_status()

        # yield the first page
        yield response.json()

        # retrieve total pages from response headers
        num_pages = int(response.headers['total-pages'])

        # iterate from second page onwards
        for page in range(2, num_pages+1):
            next_page = self.session.get(self.url,
                                         headers=self.headers,
                                         params={'page': page})
            yield next_page.json()
