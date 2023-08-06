import yaml
import os
from mkdocs.plugins import BasePlugin

from jinja2 import Template


CONFIG_KEYS = [
    'site_name',
    'site_author',
    'site_url',
    'repo_url',
    'repo_name'
]


class CodeYamlPlugin(BasePlugin):
    """
    Inject certain config variables into the markdown. Include secondary yml files
    """
    def on_page_markdown(self, markdown, config, **kwargs):
        context = {key: config.get(key) for key in CONFIG_KEYS if key in config}
        context.update(config.get('extra', {}))
        context.update(config.get('extra_yaml', {}))
        extra = config.get('extra')
        yamls = config.get('extra_yaml')
        for client in yamls:
            path = os.path.dirname(os.path.abspath(__file__))
            yml = os.path.join(os.getcwd(), '{}.yml'.format(client.get('yaml')))
            with open(yml, 'r') as f:
                contents = yaml.safe_load(f) or {}
                context.update(contents)
                extra.update(contents)
        md_template = Template(markdown)
        return md_template.render(**extra)
