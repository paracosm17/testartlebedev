import json

from django.core.management.base import BaseCommand

from api.models import Song


class Command(BaseCommand):
    help = 'Imports data from a JSON or CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the JSON or CSV file')
        parser.add_argument(
            '--force',
            action='store_true',
            help='Add data from the table even if there is already data in the database',
        )

    def handle(self, *args, **kwargs):
        path = kwargs['file']
        force = kwargs['force']
        extension: str = path.split(".")[-1]

        if extension.lower() == "json":
            with open(path, 'r') as file:
                data = json.load(file)
                if not force:
                    if Song.objects.count() >= len(data):
                        self.stdout.write(
                            self.style.WARNING("It looks like the records have already been added to the database")
                        )
                        return

                for song in data:
                    song_data: dict = song["data"]
                    Song.objects.create(
                        tags=song_data.get("tags"),
                        theme=song_data.get("theme"),
                        genretype=song_data.get("genretype"),
                        genre=song_data.get("genre"),
                        author=song_data.get("author"),
                        composer=song_data.get("composer"),
                        fullname=song_data.get("fullname"),
                        creationyear=song_data.get("creationyear"),
                    )
            self.stdout.write(self.style.SUCCESS("Successfully imported data from JSON"))

        elif extension.lower() == "csv":
            with open(path, 'r', encoding='utf-8') as file:
                lines = file.read().splitlines()
                if not force:
                    if Song.objects.count() >= len(lines[1:]):
                        self.stdout.write(
                            self.style.WARNING("It looks like the records have already been added to the database")
                        )
                        return
                for line in lines[1:]:
                    if line.startswith('"') and line.endswith('"'):
                        line = line[1:-1]
                    line = line.split(",")
                    if len(line) != 8:
                        self.stdout.write(self.style.ERROR("It looks like you have incorrect CSV table"))
                        return
                    Song.objects.create(
                        fullname=line[0],
                        composer=line[1],
                        creationyear=line[2],
                        author=line[3],
                        genre=line[4],
                        genretype=line[5],
                        theme=line[6],
                        tags=line[7]
                    )
            self.stdout.write(self.style.SUCCESS("Successfully imported data from CSV"))

        else:
            self.stdout.write(self.style.ERROR("Wrong file format! Use json or csv"))
