import pytest
from selenium import webdriver
import http.server
import socketserver
import threading
import os
from mannered_selenium.driver_wrapper import ManneredDriver
from mannered_selenium.agent_config import AgentConfig
from selenium.webdriver import ChromeOptions

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        user_agent = self.headers.get("User-Agent", "unknown")
        # set base dir for prj/tests/test_server_root
        base_dir = os.path.join(os.path.dirname(__file__), "test_server_root")
        file_path = os.path.join(base_dir, self.path.lstrip("/"))

        # use super do_GET, if not exists or not html file.
        if not os.path.exists(file_path) or not file_path.endswith(".html"):
            return super().do_GET()

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # place holder for info of User-Agent header.
        content = content.replace("{{USER_AGENT}}", user_agent)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


@pytest.fixture(scope="session")
def http_server():
    # set base dir for prj/tests/test_server_root
    base_dir = os.path.join(os.path.dirname(__file__), "test_server_root")
    Handler = lambda *args, **kwargs: CustomHandler(*args, directory=base_dir, **kwargs)
    PORT = 8000
    httpd = socketserver.TCPServer(("localhost", PORT), Handler)

    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    yield f"http://localhost:{PORT}"

    httpd.shutdown()
    thread.join()

@pytest.fixture
def star_driver():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver=ManneredDriver(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def disallowed_driver():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    config = AgentConfig(name="DisallowedBot", version="1.0")
    driver = ManneredDriver(config=config, options=options)
    yield driver
    driver.quit()

@pytest.fixture
def allowed_driver():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    config = AgentConfig(name="AllowedBot", email="test@email.com")
    driver = ManneredDriver(config=config, default_delay=3, options=options)
    yield driver
    driver.quit()