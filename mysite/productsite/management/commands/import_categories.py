from django.core.management.base import BaseCommand
import csv
from productsite.models import Category  # Update to your correct app and model path

class Command(BaseCommand):
    help = 'Loads categories from a specified CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The CSV file path')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file_path']
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                parent_name = row[0]
                subcategories = row[1:]
                parent, created = Category.objects.get_or_create(name=parent_name, parent=None)
                for subcategory_name in subcategories:
                    Category.objects.get_or_create(name=subcategory_name, parent=parent)

            self.stdout.write(self.style.SUCCESS('Successfully imported categories'))
