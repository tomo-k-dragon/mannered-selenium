import urllib.robotparser
from urllib.parse import urlparse
from .exceptions import RobotsDeniedError, RobotsNotFetchedError

class RobotsManager:
    """
    A manager class for handling robots.txt rules for multiple domains.
    
    This class caches RobotFileParser instances for each domain to avoid
    fetching robots.txt repeatedly. It provides methods to check if a URL
    is allowed to be crawled by a specific user-agent and to get the
    crawl delay defined in robots.txt.
    """

    def __init__(self):
        self.cache = {}  # domain → RobotFileParser

    def get_parser(self, url: str) -> urllib.robotparser.RobotFileParser:
        """
        Get the RobotFileParser for a given URL's domain.
        If the parser for the domain is cached, returns it from the cache.
        Otherwise, fetches the robots.txt from the domain, parses it, and caches it.
        Args:
            url (str): The URL to check.
        Returns:
            urllib.robotparser.RobotFileParser: The parser for the domain.
        Raises:
            RobotsNotFetchedError: If fetching the robots.txt fails.
        """

        parsed_url = urlparse(url)
        scheme = parsed_url.scheme
        domain = parsed_url.netloc

        if domain in self.cache:
            return self.cache[domain]

        robots_url = f"{scheme}://{domain}/robots.txt"

        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)

        try:
            rp.read()
        except Exception as e:
            raise RobotsNotFetchedError(f"Could not fetch: {robots_url}")

        self.cache[domain] = rp
        return rp

    def ensure_allowed(self, url: str, user_agent="*"):
        """
        Ensure that crawling the given URL is allowed for the specified user-agent.
        Args:
            url (str): The URL to check.
            user_agent (str): The user-agent to check against (default "*").
        Raises:
            RobotsDeniedError: If robots.txt explicitly disallows crawling this URL.
        """
        rp = self.get_parser(url)
        if not rp.can_fetch(user_agent, url):
            raise RobotsDeniedError(f"robots.txt disallows access: {url}")

    def get_crawl_delay(self, url: str, user_agent="*") -> int:
        """
        Get the crawl delay specified in robots.txt for the given user-agent.
        Args:
            url (str): The URL to check.
            user_agent (str): The user-agent to check against (default "*").
        Returns:
            int | None: Crawl delay in seconds if specified, otherwise None.
        """
        rp = self.get_parser(url)
        delay = rp.crawl_delay(user_agent)
        return delay if delay is not None else None
