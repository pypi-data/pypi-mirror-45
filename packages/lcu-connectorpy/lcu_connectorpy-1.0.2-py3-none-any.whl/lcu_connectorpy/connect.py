import sys
import psutil
import time
from pathlib import Path
from watchdog import events
from watchdog.observers import Observer
from typing import Tuple, Callable, Optional


class Lock:
    """Parses the data in the lock file and formats the result"""

    def __init__(self, path: Path):
        self.path = path
        self.data = {
            'name': None,
            'id': None,
            'port': None,
            'password': None,
            'protocol': None
        }

    def load(self) -> dict:
        """Load the lock file, store the results, and return the stored data"""
        if self.path.exists():
            data = self.path.read_text().split(':')
            self.data = {k: v for k, v in zip(self.data, data)}
        else:
            self.data = {k: None for k in self.data}

        return self.data


class LeagueClient:
    """Handles locating the executable and lock file. Platform independent."""

    name = "LeagueClient." + 'exe' if sys.platform.startswith('win') else 'app'

    def __init__(self):
        self.reset()

    def __get_process(self) -> psutil.Process:
        for p in psutil.process_iter():
            if self.name == p.name():
                return p

    def __get_lock(self) -> Lock:
        if self.process is None:
            return

        for file in self.process.open_files():
            if file.path.endswith('lockfile'):
                return Lock(Path(file.path))

    def reset(self):
        """Look for the process and lock file again"""
        self.process = self.__get_process()
        self.lock = self.__get_lock()

    def wait(self):
        """Block until a process and lock file have been found"""
        while not self.ready:
            self.reset()
            time.sleep(1)

    @property
    def ready(self) -> bool:
        return bool(self.process and self.lock)


class FileSentry(events.FileSystemEventHandler):

    def __init__(self, path: Path, callback: Callable):
        super().__init__()

        self.path = path
        self.callback = callback
        self.observer = Observer()
        self.observer.schedule(self, self.path.parent)

    def __del__(self):
        self.observer.stop()

    def on_any_event(self, event):
        if Path(event.src_path) == self.path:
            self.callback()

    def start(self):
        self.observer.start()


class Connector:
    """
    Manager for getting info required to connect to the League Client.

    example::

    ```
    import requests
    from lcu_connectorpy import Connector

    conn = Connector()
    conn.start()

    r = requests.get(
        f'{conn.url}/Help',
        auth=conn.auth,
        headers={'Accept': 'application/json'}
    )
    print(r.json())
    ```
    """

    address = '127.0.0.1'
    username = 'riot'
    port: Optional[str] = None
    password: Optional[str] = None
    protocol: Optional[str] = None
    id: Optional[str] = None

    def __init__(self):
        self.client = LeagueClient()
        self.sentry: Optional[FileSentry] = None

    def __update(self):
        self.__dict__.update(self.client.lock.load())

    def start(self):
        """Start watching for the client. Blocks until found."""
        self.client.wait()
        self.__update()

        self.sentry = FileSentry(self.client.lock.path, self.__update)

    @property
    def connected(self) -> bool:
        """Established connection, data is ready."""
        return self.client.ready

    @property
    def url(self) -> str:
        """A url using the current lock file data"""
        return f'{self.protocol}://{self.address}:{self.port}'

    @property
    def auth(self) -> Tuple[str]:
        """A tuple (user, password) with the latest credentials"""
        return (self.username, self.password)
