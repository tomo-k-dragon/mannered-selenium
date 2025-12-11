# mannered-selenium

`mannered-selenium` is a Python library that extends Selenium WebDriver.  
It allows you to perform polite web scraping by automatically following the rules defined in robots.txt.

---
## Feature
- Automatically check if scraping is allowed based on robots.txt. Raises `RobotsDeniedError` if access is disallowed.
- Automatically controls the access interval based on `Crawl-delay` in robots.txt or your `default_delay` setting.
- Automatically manages User-Agent settings and adds it to the WebDriver headers, e.g., `agent-name/version (email)`.
- Wrapper class for WebDriver, so you can use it like a regular Selenium WebDriver.
    
---
## Prerequisites
To use selenium, you need a WebDriver that matches your browser.
If you use Google Chrome, please install ChromeDriver.
- ChromeDriver version must match your Chrome browser version
- Make sure the ChromeDriver binary is added to your system PATH

---
## Installation
```bash
pip install git+https://github.com/tomo-k-dragon/mannered-selenium.git
```

---
## Usage
```python
from mannered_selenium.driver_wrapper import ManneredDriver
from mannered_selenium.agent_config import AgentConfig

# set agent info.
config = AgentConfig(name="mybot", version="1.0", email="mybot@example.com")

# create driver.
driver = ManneredDriver(config=config, default_delay=2)

# access with automatically check based on robots.txt.
driver.get("https://example.com")

```

---
## License
MIT License
