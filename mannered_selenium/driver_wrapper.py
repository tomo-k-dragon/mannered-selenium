from selenium import webdriver
from .robots import RobotsManager
from .rate_limiter import RateLimiter
from .agent_config import AgentConfig
from typing import Optional
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class ManneredDriver:
    config = None
    def __init__(
            self, 
            options: Optional[Options] = None, 
            service: Optional[Service] = None, 
            keep_alive: Optional[bool] = True,
            config: Optional[AgentConfig] = None,
            default_delay: Optional[int] = None
        ):
        """
        create instance of ManneredDriver.
        Args:
            options: This takes an instance of ChromeOptions.
            service: Service object for handling the browser driver if you need to pass extra details.
            keep_alive: Whether to configure ChromeRemoteConnection to use HTTP keep-alive.
            default_delay: wait second each driver.get. if target site crawl-delay of robots.txt is set, it will be ignored.
        """

        # add User-Agent header to driver.
        if config:
            self.config = config
        else:
            self.config = AgentConfig(name = "*")

        # add agent header through the config
        if options is None:
            options = Options()
        options.add_argument(f"user-agent={self.config.build_user_agent()}")

        self.driver = webdriver.Chrome(options=options, service=service, keep_alive=keep_alive)
        self.robots = RobotsManager()
        self.rate = RateLimiter(default_delay=default_delay)


    def get(self, url: str):
        # if not allowed, raise RobotsDeniedError from method.
        self.robots.ensure_allowed(url, user_agent=self.config.name)

        # wait for delay
        cd = self.robots.get_crawl_delay(url, self.config.name)
        self.rate.wait(crawl_delay=cd)

        return self.driver.get(url)

    # wrap webdriver.
    def __getattr__(self, name):
        return getattr(self.driver, name)
