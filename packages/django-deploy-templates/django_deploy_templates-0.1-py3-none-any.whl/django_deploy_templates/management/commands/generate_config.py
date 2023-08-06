import os
from jinja2 import Environment, FileSystemLoader
import glob
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Generating config files with deploy templates'

    def handle(self, **options):

        if not settings.ALLOWED_HOSTS:
            return 'Ничего не сделали, заполни ALLOWED_HOSTS в настройках'

        jinja_env = Environment(
            loader=FileSystemLoader(settings.DEPLOY_TEMPLATES_DIR),
        )

        for filepath in glob.glob(os.path.join(settings.DEPLOY_TEMPLATES_DIR, '*.jinja2'), recursive=True):
            template_name = filepath.replace(f"{settings.DEPLOY_TEMPLATES_DIR}{os.sep}", '')
            template = jinja_env.get_template(template_name)
            config_filename = os.path.splitext(template_name)[0]

            generated_config = template.render({'settings': settings})

            with open(os.path.join(settings.DEPLOY_CONF_DIR, config_filename), 'w', encoding='utf8') as f:
                f.write(generated_config)
