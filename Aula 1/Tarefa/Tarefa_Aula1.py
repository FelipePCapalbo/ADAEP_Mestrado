# Felipe Papa Capalbo - 792232
# Tarefa Aula 1
# Nota: A ideia é dividir em duas imagens: uma com as stopwords e outra sem

from wordcloud import WordCloud
import matplotlib.pyplot as plt

def separar_stopwords(lista_completa_palavras):

    # Lista de stopwords criada manualmente
    stopwords = {
        'a', 'à', 'às', 'agora', 'ainda', 'ali', 'aquele', 'aquela', 'aqueles', 'aquelas',
        'aquilo', 'as', 'ao', 'aos', 'aí', 'até', 'com', 'como', 'da', 'das', 'de',
        'dele', 'dela', 'deles', 'delas', 'depois', 'do', 'dos', 'e', 'ela', 'elas',
        'ele', 'eles', 'em', 'então', 'era', 'eram', 'essa', 'essas', 'esse', 'esses',
        'esta', 'estas', 'este', 'estes', 'eu', 'foi', 'ia', 'isso', 'isto', 'já',
        'lá', 'lhe', 'lhes', 'mas', 'me', 'meu', 'meus', 'minha', 'minhas', 'mais',
        'na', 'nas', 'não', 'nem', 'nesse', 'neste', 'no', 'nos', 'nossa', 'nossas',
        'nosso', 'nossos', 'num', 'numa', 'o', 'os', 'ou', 'outra', 'outro', 'para',
        'pela', 'pelas', 'pelo', 'pelos', 'por', 'pra', 'pras', 'pro', 'quais', 'qual',
        'quando', 'que', 'quem', 'se', 'sem', 'ser', 'seu', 'seus', 'são', 'só',
        'sua', 'suas', 'sob', 'sobre', 'tá', 'tal', 'também', 'tanto', 'te', 'tem',
        'ter', 'teu', 'teus', 'tinha', 'toda', 'todas', 'todo', 'todos', 'tua', 'tuas',
        'tudo', 'um', 'uma', 'uns', 'umas', 'você', 'vou'
    }

    # Prepara as listas vazias
    lista_sem_stopwords = []
    lista_com_stopwords = []

    # Itera sobre cada palavra da letra
    for palavra in lista_completa_palavras:
        # Converte a palavra para minúscula para a verificação
        if palavra.lower() in stopwords:
            lista_com_stopwords.append(palavra)
        else:
            lista_sem_stopwords.append(palavra)

    # Retorna as duas listas
    return lista_sem_stopwords, lista_com_stopwords

# Referencia o arquivo da letra
arquivo_FaroesteCaboclo = open("FaroesteCaboclo.txt")

# Armazena a letra dentro da variável "letra_FaroesteCaboclo"
letra_FaroesteCaboclo = arquivo_FaroesteCaboclo.read()

# Libera o recurso da memoria
arquivo_FaroesteCaboclo.close()

# Aplica o split à variável de texto com a letra toda e separa em lista para cada palavra
listaLetra_FaroesteCaboclo = letra_FaroesteCaboclo.split()

listaLetra_semStopWords, listaLetra_comStopWords = separar_stopwords(listaLetra_FaroesteCaboclo)

# Junta as palavras, separando-as por espaço, para plotar
letra_semStopWords = ' '.join(listaLetra_semStopWords)
letra_comStopWords = ' '.join(listaLetra_comStopWords)

# Gera a word cloud 3Menos (agora são as stopwords)
wordcloud_semStopWords = WordCloud(
    width=800,
    height=400,
    background_color='white',
    colormap='plasma',  # Paleta de cores plasma
).generate(letra_semStopWords)

# Gera a word cloud Mais3 (agora são as palavras principais)
wordcloud_comStopWords = WordCloud(
    width=800,
    height=400,
    background_color='white',
    colormap='inferno',  # Paleta de cores inferno
).generate(letra_comStopWords)

# Exibe uma das imagens geradas (a das palavras principais)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_comStopWords, interpolation='bilinear')
plt.axis("off")
plt.show()

# Salva direto em arquivo PNG
wordcloud_semStopWords.to_file("wordcloud_semStopWords.png")
wordcloud_comStopWords.to_file("wordcloud_comStopWords.png")