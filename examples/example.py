from mannered_selenium.agent_config import AgentConfig
from mannered_selenium.driver_wrapper import ManneredDriver
from selenium.webdriver.common.by import By

config = AgentConfig(name="my-agent", version="1.0", email="test@email.com")
driver: ManneredDriver = ManneredDriver(config=config, default_delay = 2)

driver.get("https://target-site.com/top")
...

driver.get("https://target-site.com/detail-page")

driver.quit()
