class RobotsDeniedError(Exception):
    """Access denied by robots.txt."""

class RobotsNotFetchedError(Exception):
    """Failed to fetch robots.txt."""

