from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.management.commands import search_index_command


class Command(BaseCommand):
    help = 'Build Elasticsearch search indices'
    
    def handle(self, *args, **options):
        self.stdout.write('Building Elasticsearch indices...')
        
        try:
            # Use the built-in search_index command
            search_index_command.Command().handle(action='rebuild', force=True)
            self.stdout.write(
                self.style.SUCCESS('Successfully built Elasticsearch indices')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error building indices: {str(e)}')
            )
            self.stdout.write(
                'Make sure Elasticsearch is running on localhost:9200'
            )
