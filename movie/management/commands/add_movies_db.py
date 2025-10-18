from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json

class Command(BaseCommand):
    help = "Load movies from movies.json into the Movie model"

    def handle(self, *args, **kwargs):
        # Ruta al JSON en la misma carpeta del comando
        json_file_path = os.path.join(os.path.dirname(__file__), "movies.json")

        # Cargar datos desde el archivo JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            movies = json.load(file)

        # Agregar películas a la base de datos
        for i, movie in enumerate(movies[:10]):  # solo las 10 primeras
            exist = Movie.objects.filter(title=movie.get('movie_title', '').strip()).first()
            if not exist:
                Movie.objects.create(
                title=movie.get('movie_title', 'Título desconocido').strip(),
                image='movie/images/default.jpg',
                genre=movie.get('genres', 'Género desconocido'),
                year=movie.get('title_year') or 0,
                 description=(movie.get('plot_keywords') or 'Sin descripción')
)

                

        self.stdout.write(self.style.SUCCESS("Películas cargadas con éxito"))

