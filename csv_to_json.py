import pandas as pd
import json

# Leer el CSV
df = pd.read_csv('movies_initial.csv')

# Exportar a JSON con indentación (más legible)
df.to_json('movies.json', orient='records', force_ascii=False, indent=4)

# Cargar el JSON
with open('movies.json', 'r', encoding='utf-8') as file:
    movies = json.load(file)

print("Primer registro:", movies[0])
