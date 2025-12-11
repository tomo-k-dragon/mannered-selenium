import time
from mannered_selenium.driver_wrapper import ManneredDriver
from mannered_selenium.agent_config import AgentConfig
from mannered_selenium.exceptions import RobotsDeniedError
from tests.conftest import http_server
from selenium.webdriver.common.by import By

def test_star_driver(http_server, star_driver):
    DELAY=2
    driver = star_driver
    time0 = time.time()
    driver.get(f"{http_server}/index.html")

    agent_label = driver.find_element(By.TAG_NAME, "p")
    assert agent_label.text == "User-Agent: *"
    driver.get(f"{http_server}/allowed.html")
    now = time.time()
    assert now - time0 > DELAY, f"Violate interval of robots crawl-delay {DELAY}."

    try:
        driver.get(f"{http_server}/global-disallowed.html")
        assert False, "Bad access to global-disallowed.html."
    except RobotsDeniedError:
        pass


def test_disallowed_driver(http_server, disallowed_driver):
    DELAY=3
    driver = disallowed_driver
    time0 = time.time()
    driver.get(f"{http_server}/index.html")

    agent_label = driver.find_element(By.TAG_NAME, "p")
    assert agent_label.text == "User-Agent: DisallowedBot/1.0"
    time1 = time.time()
    driver.get(f"{http_server}/allowed.html")
    now = time.time()
    assert now - time0 > DELAY, f"Violate interval of robots crawl-delay {DELAY}."

    try:
        driver.get(f"{http_server}/disallowed.html")
        assert False, "Disallowed agent access to the disallowed page."
    except RobotsDeniedError:
        pass

def test_allowed_driver(http_server, allowed_driver):
    DELAY=2
    driver = allowed_driver
    time0 = time.time()
    driver.get(f"{http_server}/index.html")

    agent_label = driver.find_element(By.TAG_NAME, "p")
    assert agent_label.text == "User-Agent: AllowedBot (test@email.com)"

    time1 = time.time()
    driver.get(f"{http_server}/allowed.html")
    now = time.time()
    assert now - time0 > DELAY, f"Violate interval of robots crawl-delay {DELAY}."

    driver.get(f"{http_server}/disallowed.html")
    now = time.time()
    assert now - time1 > DELAY, f"Violate interval of robots crawl-delay {DELAY}."


def test_agent_config():
    config = AgentConfig(name="test_agent",version="1.0",email="test@email.com")
    assert config.build_user_agent() == "test_agent/1.0 (test@email.com)"

    config = AgentConfig(name=None, version=None, email=None)
    assert config.build_user_agent() == "*"

    config = AgentConfig(name="test_agent", version=None, email=None)
    assert config.build_user_agent() == "test_agent"

    config = AgentConfig(name="test_agent", version="1.0", email=None)
    assert config.build_user_agent() == "test_agent/1.0"

    config = AgentConfig(name="test_agent", version=None, email="test@email.com")
    assert config.build_user_agent() == "test_agent (test@email.com)"

    # version but not name.
    try:
        AgentConfig(name=None, version="1.0", email=None).build_user_agent()
        assert False, "ValueError expected"
    except ValueError:
        pass

    # version and email, but not name.
    try:
        AgentConfig(name=None, version="1.0", email="test@email.com").build_user_agent()
        assert False, "ValueError expected"
    except ValueError:
        pass

    # only email.
    config = AgentConfig(name=None, version=None, email="test@email.com")
    assert config.build_user_agent() == "* (test@email.com)"