# Felipe Papa Capalbo - 792232
# Tarefa Aula 1
# Nota: A ideia é dividir em duas imagens: palavras com menos de 3 letras e mais de 3 letras

# Referencia o arquivo da letra
arquivo_FaroesteCaboclo = open("FaroesteCaboclo.txt")

# Armazena a letra dentro da variável "letra_FaroesteCaboclo"
letra_FaroesteCaboclo = arquivo_FaroesteCaboclo.read()

# Libera o recurso da memoria
arquivo_FaroesteCaboclo.close()

# Aplica o split à variável de texto com a letra toda e separa em lista para cada palavra
listaLetra_FaroesteCaboclo = letra_FaroesteCaboclo.split()

# Separa em lista de palavras com mais e menos de 3 letras
listaLetra_3menos = []
listaLetra_Mais3 = []

for palavra in listaLetra_FaroesteCaboclo:
    if len(palavra) <= 3:
        listaLetra_3menos.append(palavra)
    else:
        listaLetra_Mais3.append(palavra)

# Junta as palavras, separando-as por espaço, para plotar
letra_3Menos = ' '.join(listaLetra_3menos)
letra_Mais3 = ' '.join(listaLetra_Mais3)

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import random

# Gera a word cloud 3Menos
wordcloud_3Menos = WordCloud(
    width=800,
    height=400,
    background_color='white',
    colormap='plasma',  # Paleta de cores plasma
).generate(letra_3Menos)

# Gera a word cloud Mais3
wordcloud_Mais3 = WordCloud(
    width=800,
    height=400,
    background_color='white',
    colormap='inferno',  # Paleta de cores inferno
).generate(letra_Mais3)

# Exibe uma das imagens geradas
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_Mais3, interpolation='bilinear')
plt.axis("off")
plt.show()

# Salva direto em arquivo PNG
wordcloud_3Menos.to_file("wordcloud_3menos.png")
wordcloud_Mais3.to_file("wordcloud_mais3.png")
