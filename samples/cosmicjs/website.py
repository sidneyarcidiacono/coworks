import mimetypes
import os
from pathlib import Path

from coworks import TechMicroService
from coworks.cws.runner import CwsRunner, run_with_reloader
from jinja2 import Environment, FileSystemLoader, select_autoescape

from config import DevConfig
from cosmicjs import CosmicCmsClient


class WebsiteMicroService(TechMicroService):

    def __init__(self, env=None, **kwargs):
        super().__init__(name="website-handless", **kwargs)
        self.jinja_env = env or Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(['html', 'xml'], default_for_string=True)
        )
        self.cosmic_client = self.workspace = None

        @self.before_first_activation
        def init(*args):
            self.workspace = os.getenv('WORKSPACE')
            self.cosmic_client = CosmicCmsClient()

    def get(self):
        assets_url = os.getenv('ASSETS_URL')
        data = self.cosmic_client.get_home()
        template_filename = 'home.j2'
        template = self.jinja_env.get_template(template_filename)
        headers = {'Content-Type': 'text/html; charset=utf-8'}
        return template.render(assets_url=assets_url, **data), 200, headers

    def get_assets_css(self, filename):
        return self.return_file(f'assets/css/{filename}')

    def get_assets_css_images(self, filename):
        return self.return_file(f'assets/css/images/{filename}')

    def get_assets_js(self, filename):
        return self.return_file(f'assets/js/{filename}')

    def get_assets_webfonts(self, filename):
        return self.return_file(f'assets/webfonts/{filename}')

    def get_images(self, filename):
        return self.return_file(f'images/{filename}')

    @staticmethod
    def return_file(file):
        file = Path.cwd() / file
        mt = mimetypes.guess_type(file)
        content = file.read_bytes()
        try:
            return content.decode('utf-8'), 200, {'Content-Type': mt[0]}
        except:
            return content, 200, {'Content-Type': mt[0]}


app = WebsiteMicroService(configs=[DevConfig()])
CwsRunner(app)

if __name__ == '__main__':
    run_with_reloader(app, project_dir='src', module='website', workspace='local')
