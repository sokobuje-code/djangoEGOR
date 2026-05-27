import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egorcore.settings')
django.setup()

from mainhub.models import Book

def main():
    b = Book.objects.create(title='книжки', author='Тест')
    print('Created:', b)
    print('Count:', Book.objects.count())
    print('First:', Book.objects.first())

if __name__ == '__main__':
    main()
