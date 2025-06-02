import pandas as pd

# Cargar datos desde Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
tables = pd.read_html(url)
sp500_df = tables[0]
print(sp500_df.head(3))

# Seleccionar columnas relevantes
sp500_df = sp500_df[['Symbol', 'Date added']]
sp500_df = sp500_df.dropna(subset=['Date added'])

# Convertir a fecha y extraer año
sp500_df['YearAdded'] = pd.to_datetime(sp500_df['Date added'], errors='coerce').dt.year

# Excluir 1957 y contar adiciones por año
additions_per_year = sp500_df[sp500_df['YearAdded'] != 1957]['YearAdded'].value_counts().sort_index()
max_additions_year = additions_per_year[additions_per_year == additions_per_year.max()].index.max()

# Empresas con más de 20 años en el índice
current_year = pd.Timestamp.now().year
sp500_df['YearsInIndex'] = current_year - sp500_df['YearAdded']
over_20_years_count = (sp500_df['YearsInIndex'] > 20).sum()

print("Año con más adiciones (excluyendo 1957):", max_additions_year)
print("Número de empresas actuales con más de 20 años en el índice:", over_20_years_count)