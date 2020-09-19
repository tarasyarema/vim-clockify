import pynvim as neovim
import requests
import json

from dotenv import load_dotenv, find_dotenv
from os import getenv, environ


CLOCKIFY_API_URL = "https://api.clockify.me/api/v1"


@neovim.plugin
class Main(object):
    def __init__(self, nvim):
        load_dotenv(find_dotenv())

        self.nvim = nvim
        self._clockify = {
            'init': False
        }

        self.api_url = getenv("CLOCKIFY_API_URL")
        if not self.api_url:
            self.api_url = CLOCKIFY_API_URL

        self.api_key = getenv("CLOCKIFY_API_KEY")

        if self.api_key:
            self.init_clockify()

    def echo(self, contents):
        self.nvim.command(f"echo \"{contents}\"")

    def error(self, contents):
        self.echo(f"ERROR: {contents}")

    def get_user(self):
        url = f"{self.api_url}/user"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code != 200:
            raise Exception(
                f"Could not get user, status code is {resp.status_code}")

        return resp.json()

    def init_clockify(self):
        self.headers = {"X-Api-Key": self.api_key}

        try:
            self.user = self.get_user()
        except Exception as e:
            self.error(f"Could not init Clockify plugin: {e}")
            return

        # Setup the key as env now,
        # after acorrect API call
        if not getenv("CLOCKIFY_API_KEY"):
            environ["CLOCKIFY_API_KEY"] = self.api_key

        self._clockify['init'] = True

    @neovim.command('ClockifyKey', nargs='*', range='')
    def clockify_key(self, args, range):
        if self.api_key:
            self.echo("Clockify API key already setup")
            return

        if len(args) == 0:
            self.error("The given API key is empty")
            return

        key = args[0]
        if not key:
            self.error("The given API key is empty")
            return

        self.api_key = key
        self.echo("Clockify API key setup")

        self.init_clockify()

    @neovim.command('Clockify')
    def clockify(self):
        if not self._clockify['init']:
            self.echo('Clockify is not setup')
            return

        bufh = self.nvim.api.create_buf(False, True)

        w = self.nvim.api.win_get_width(0)
        _ = self.nvim.api.win_get_height(0)

        width, height = 20, 5
        row = 1
        col = w - width

        _ = self.nvim.api.open_win(
            bufh,
            False,
            {
                "style": 'minimal',
                "relative": 'win',
                "row": row,
                "col": col,
                "width": width,
                "height": height,
            }
        )

        self.nvim.api.buf_set_lines(
            bufh,
            0,
            2,
            False,
            [
                "",
                f" Hi, {self.user['name']}",
            ],
        )
