from datetime import timedelta

from django.core.management import call_command
from django.db import connection
from django.test import TestCase

from test_project import models


class TestDjangoSecondsField(TestCase):

    @staticmethod
    def setUp():
        call_command('loaddata', 'category', database='default', verbosity=0)
        call_command('loaddata', 'note', database='default', verbosity=0)

    def test_model_object(self):
        note = models.Note.objects.get(pk=1)
        self.assertEqual(note.id, 1)
        self.assertEqual(note.ttl, timedelta(seconds=3600))
        self.assertEqual(str(note.ttl), '1:00:00')

    def test_raw_query(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT ttl FROM test_project_note WHERE id = 1')
            row = cursor.fetchone()
            self.assertEqual(row[0], 3600)
