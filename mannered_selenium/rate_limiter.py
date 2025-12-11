import time
from .agent_config import AgentConfig

class RateLimiter:
    """
    class to control interval of each access.
    """
    def __init__(self, default_delay):
        """
        create instance of RateLimiter to control interval of each access.
        """
        self.last_access_ts = 0
        if default_delay and default_delay > 1:
            self.default_delay = default_delay
        else:
            self.default_delay = 1

    def wait(self, crawl_delay=None):
        """
        Wait until the next access interval.
        """
        delay = crawl_delay or self.default_delay

        now = time.time()
        elapsed = now - self.last_access_ts

        if elapsed < delay:
            time.sleep(delay - elapsed)

        self.last_access_ts = time.time()
