from typing import Protocol, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class WebDriverLike(Protocol):
    def get(self, url: str) -> None:
        """ Navigate the browser to the specified URL in the current window or
        tab. Before navigating check if it is allowed and applies a delay execution based on the robots.txt of specified URL."""
        ...

    def back(self) -> None: 
        """Delegates to selenium.webdriver.remote.webdriver.WebDriver.back.""" 
        ...

    def forward(self) -> None: 
        """Delegates to selenium.webdriver.remote.webdriver.WebDriver.forward.""" 
        ...

    def refresh(self) -> None: 
        """Delegates to selenium.webdriver.remote.webdriver.WebDriver.refresh.""" 
        ...

    def find_element(self, by=By.ID, value: Optional[str] = None) -> WebElement:
        """Delegates to selenium.webdriver.remote.webdriver.WebDriver.find_element."""
        ...

    def find_elements(self, by=By.ID, value: Optional[str] = None) -> list[WebElement]: 
        """Delegates to selenium.webdriver.remote.webdriver.WebDriver.find_elements."""
        ...

    def execute_script(self, script: str, *args): 
        """Delegates to selenium.webdriver.remote.webdriver.WebDriver.execute_script."""
        ...

    @property
    def current_url(self) -> str: 
        """Delegates to selenium.webdriver.remote.webdriver.WebDriver.current_url."""
        ...

    @property
    def title(self) -> str: 
        """Delegates to selenium.webdriver.remote.webdriver.WebDriver.title."""
        ...

    def close(self) -> None: 
        """Delegates to selenium.webdriver.remote.webdriver.WebDriver.close."""
        ...

    def quit(self) -> None: 
        """Delegates to selenium.webdriver.remote.webdriver.WebDriver.quit."""
        ...
    