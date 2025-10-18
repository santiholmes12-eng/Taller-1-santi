from django.shortcuts import render
from django.http import HttpResponse
import matplotlib
from .models import Movie
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render


def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {
        'searchTerm': searchTerm,
        'movies': movies
    })


def about(request):
    return render(request, 'about.html')


def statistics_view(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}

    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    # Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})


