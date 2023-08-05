import psutil
import time
import yaml
from pathlib import Path
from watchdog import events
from watchdog.observers import Observer
from typing import Tuple, Callable, Optional


class RestartRequiredError(Exception):
    def __init__(self):
        super().__init__("Please restart your League of Legends Client")


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
        self.load()

    def load(self) -> dict:
        """Load the lock file, store the results, and return the stored data"""
        if self.path.exists():
            data = self.path.read_text().split(':')
            self.data = {k: v for k, v in zip(self.data, data)}
        else:
            self.data = {k: None for k in self.data}

        return self.data

    @property
    def ready(self) -> bool:
        return all(self.data.values())


class LeagueClient:
    """Handles locating the executable and lock file. Platform independent."""

    name = "LeagueClient." + 'exe' if psutil.WINDOWS else 'app'

    def __init__(self):
        self.reset()

    def __get_process(self) -> psutil.Process:
        for p in psutil.process_iter():
            if self.name == p.name():
                return p

    def __get_lock(self) -> Lock:
        if self.process is None:
            return

        try:
            files = self.process.open_files()
        except psutil.AccessDenied as e:
            self.__enable_swagger()
            raise RestartRequiredError from e

        for file in files:
            if file.path.endswith('lockfile'):
                return Lock(Path(file.path))

    def __enable_swagger(self):
        yaml_fp = Path(self.process.exe()).with_name('system.yaml')
        yl = yaml.load(yaml_fp.read_text())
        yl['enable_swagger'] = True

        yaml_fp.write_text(yaml.dump(yl))

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
        return bool(self.process and self.lock and self.lock.ready)


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

    def update(self):
        if not self.client.lock:
            return
        for k, v in self.client.lock.load().items():
            setattr(self, k, v)

    def start(self):
        """Start watching for the client. Blocks until found."""
        self.client.wait()
        self.update()

        self.sentry = FileSentry(self.client.lock.path, self.update)

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
