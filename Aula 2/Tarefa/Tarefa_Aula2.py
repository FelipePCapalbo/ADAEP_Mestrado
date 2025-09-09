import pdfplumber
import pandas as pd
import re

# Limites das colunas da tabela (coordenadas X)
colunas_pdf = {
    'nome': (55, 152),
    'localidade': (170, 248), 
    'curso': (249, 380),
    'opcao_curricular': (383, 528),
    'perfil': (590, 670),
    'perfil_continuacao': (560, 670),
    'status': (670, 720),
    'egresso': (695, 820)
}

# regex pré-compiladas
_re_ra = re.compile(r'^\d{6}$')
_re_data = re.compile(r'^\d{4}/\d$')
_re_status = re.compile(r'^\d{1,2}$')

def extrair_dados(arquivo_pdf):
    registros_extraidos = []

    with pdfplumber.open(arquivo_pdf) as pdf:
        for pagina in pdf.pages:
            # ordena uma vez por (top, x0)
            palavras = sorted(pagina.extract_words(), key=lambda w: (w['top'], w['x0']))

            # Encontrar números RA (início de cada registro) - sem filtro de posição
            numeros_RA = [p for p in palavras if _re_ra.match(p['text'])]

            # print(numeros_RA)

            # helper: filtra palavras de um “bloco” vertical
            def _bloco(l_ini, l_fim):
                return [p for p in palavras if l_ini <= p['top'] < l_fim]

            # helper: coleta textos em uma faixa horizontal na linha principal
            def _coletar_faixa(bloco, faixa, linha_ref, margem=5, excluir_datas=False, excluir_tokens=None):
                itens = []
                for p in bloco:
                    if faixa[0] <= p['x0'] <= faixa[1] and abs(p['top'] - linha_ref) < margem:
                        texto = p['text']
                        
                        # Filtrar textos de rodapé/cabeçalho específicos
                        if (texto in ['Página', 'Total', 'Emitido', 'às', '2143'] or
                            'Página' in texto or 'Total' in texto):
                            continue
                        
                        # Filtrar números de página isolados (quando próximos de "de")
                        if re.match(r'^\d{1,4}$', texto):
                            # Verificar se está próximo de palavra "de" (contexto de rodapé)
                            contexto_pagina = False
                            for outro_p in bloco:
                                if (abs(outro_p['x0'] - p['x0']) < 30 and 
                                    abs(outro_p['top'] - p['top']) < 5 and
                                    outro_p['text'] == 'de'):
                                    contexto_pagina = True
                                    break
                            if contexto_pagina:
                                continue
                        
                        # Filtrar "de" apenas quando está isolado (rodapé) 
                        if texto == 'de':
                            # Verificar se está em contexto de rodapé (próximo a números)
                            contexto_rodape = False
                            for outro_p in bloco:
                                if (abs(outro_p['x0'] - p['x0']) < 50 and 
                                    abs(outro_p['top'] - p['top']) < 5 and
                                    re.match(r'^\d{2,4}$', outro_p['text'])):
                                    contexto_rodape = True
                                    break
                            if contexto_rodape:
                                continue
                            
                        if excluir_datas and _re_data.match(texto):
                            continue
                        if excluir_tokens and texto in excluir_tokens:
                            continue
                        itens.append(texto)
                return ' '.join(itens)

            for i, registro_RA in enumerate(numeros_RA):
                posicao_vertical_RA = registro_RA['top']
                linha_inicio = posicao_vertical_RA

                if i + 1 < len(numeros_RA):
                    linha_fim = numeros_RA[i + 1]['top']
                else:
                    linha_fim = linha_inicio + 50

                palavras_estudante = _bloco(linha_inicio, linha_fim)
                if not palavras_estudante:
                    continue

                # linha principal = menor top do bloco
                linha_principal = min(p['top'] for p in palavras_estudante)

                # datas do registro
                datas = [p['text'] for p in palavras_estudante if _re_data.match(p['text'])]

                # Nome completo do estudante
                nome = _coletar_faixa(palavras_estudante, colunas_pdf['nome'], linha_principal)

                # Localidade
                localidade = _coletar_faixa(palavras_estudante, colunas_pdf['localidade'], linha_principal)

                # Curso
                curso = _coletar_faixa(palavras_estudante, colunas_pdf['curso'], linha_principal)

                # Opção Curricular (sem datas)
                opcao = _coletar_faixa(
                    palavras_estudante, colunas_pdf['opcao_curricular'], linha_principal, excluir_datas=True
                )

                # Perfil (inclui continuação)
                perfil_palavras = []
                for p in palavras_estudante:
                    texto = p['text']
                    
                    # Filtrar textos de rodapé/cabeçalho específicos
                    if (texto in ['Página', 'Total', 'Emitido', 'às', '2143'] or
                        'Página' in texto or 'Total' in texto):
                        continue
                    
                    # Filtrar números de página isolados (quando próximos de "de")
                    if re.match(r'^\d{1,4}$', texto):
                        contexto_pagina = False
                        for outro_p in palavras_estudante:
                            if (abs(outro_p['x0'] - p['x0']) < 30 and 
                                abs(outro_p['top'] - p['top']) < 5 and
                                outro_p['text'] == 'de'):
                                contexto_pagina = True
                                break
                        if contexto_pagina:
                            continue
                    
                    # Filtrar "de" apenas quando está em contexto de rodapé
                    if texto == 'de':
                        contexto_rodape = False
                        for outro_p in palavras_estudante:
                            if (abs(outro_p['x0'] - p['x0']) < 50 and 
                                abs(outro_p['top'] - p['top']) < 5 and
                                re.match(r'^\d{2,4}$', outro_p['text'])):
                                contexto_rodape = True
                                break
                        if contexto_rodape:
                            continue
                    
                    if colunas_pdf['perfil'][0] <= p['x0'] <= colunas_pdf['perfil'][1]:
                        perfil_palavras.append(texto)
                    elif p['top'] > linha_principal + 5 and \
                         colunas_pdf['perfil_continuacao'][0] <= p['x0'] <= colunas_pdf['perfil_continuacao'][1]:
                        perfil_palavras.append(texto)
                perfil = ' '.join(perfil_palavras)

                # Código de status (número isolado)
                codigo_status = ''
                for p in palavras_estudante:
                    if colunas_pdf['status'][0] <= p['x0'] <= colunas_pdf['status'][1] and _re_status.match(p['text']):
                        codigo_status = p['text']
                        break

                # Situação de egresso (texto sem datas)
                egresso_palavras = []
                for p in palavras_estudante:
                    texto = p['text']
                    
                    # Filtrar textos de rodapé/cabeçalho e datas
                    if (_re_data.match(texto) or 
                        texto in ['Página', 'Total', 'Emitido', 'às', '2143'] or
                        'Página' in texto or 'Total' in texto):
                        continue
                    
                    # Filtrar números de página isolados (quando próximos de "de")
                    if re.match(r'^\d{1,4}$', texto):
                        contexto_pagina = False
                        for outro_p in palavras_estudante:
                            if (abs(outro_p['x0'] - p['x0']) < 30 and 
                                abs(outro_p['top'] - p['top']) < 5 and
                                outro_p['text'] == 'de'):
                                contexto_pagina = True
                                break
                        if contexto_pagina:
                            continue
                    
                    # Filtrar "de" apenas quando está em contexto de rodapé
                    if texto == 'de':
                        contexto_rodape = False
                        for outro_p in palavras_estudante:
                            if (abs(outro_p['x0'] - p['x0']) < 50 and 
                                abs(outro_p['top'] - p['top']) < 5 and
                                re.match(r'^\d{2,4}$', outro_p['text'])):
                                contexto_rodape = True
                                break
                        if contexto_rodape:
                            continue
                        
                    if 695 <= p['x0'] <= 780:
                        egresso_palavras.append(texto)
                situacao_egresso = ' '.join(egresso_palavras)

                # Data de conclusão (última coluna)
                data_conclusao = ''
                for p in palavras_estudante:
                    if 780 <= p['x0'] <= 820 and _re_data.match(p['text']):
                        data_conclusao = p['text']
                        break

                # Organizar as datas encontradas
                primeira_data = ''
                if len(datas) > 0:
                    primeira_data = datas[0]

                segunda_data = primeira_data
                if len(datas) > 1:
                    segunda_data = datas[1]

                # Montar campo de ingresso (data + perfil)
                if segunda_data and perfil:
                    ingresso_completo = segunda_data + ' ' + perfil
                else:
                    ingresso_completo = ''
                    if segunda_data:
                        ingresso_completo = segunda_data
                    elif perfil:
                        ingresso_completo = perfil

                # Criar registro completo do estudante
                numero_RA = registro_RA['text']
                registro = {
                    'Nº UFSCar': numero_RA,
                    'Nome': nome,
                    'Localidade Educacional': localidade,
                    'Curso': curso,
                    'Opção Curricular': opcao,
                    'Matriz Curricular': primeira_data,
                    'Ingresso': ingresso_completo,
                    'Perfil': codigo_status,
                    'Status': situacao_egresso,
                    'Egresso': data_conclusao
                }

                registros_extraidos.append(registro)

    colunas = ['Nº UFSCar', 'Nome', 'Localidade Educacional', 'Curso', 'Opção Curricular',
               'Matriz Curricular', 'Ingresso', 'Perfil', 'Status', 'Egresso']

    return pd.DataFrame(registros_extraidos)[colunas]


# Executar extração e salvar
dados = extrair_dados("dadosAcademicosEstudantis.pdf")
dados.to_csv("dados_academicos_organizados.csv", index=False)

# Carregar dados para análise
df = dados

# Limpeza de dados: remover RAs duplicados mantendo matriz mais atual
print(f"Antes da limpeza: {len(df)} registros")
df_limpo = df.sort_values(['Nº UFSCar', 'Matriz Curricular']).drop_duplicates('Nº UFSCar', keep='last')
print(f"Após limpeza: {len(df_limpo)} registros ({len(df) - len(df_limpo)} duplicados removidos)")
df = df_limpo

# Análise dos dados extraídos
import matplotlib.pyplot as plt

# 1) Quantos alunos se formam por ano em média?
formados = df[df['Status'] == 'Formado']
formados_por_ano = formados['Egresso'].str[:4].value_counts().sort_index()
media_formados = formados_por_ano.mean()
print(f"1) {media_formados:.1f} alunos se formam por ano em média")

# Histograma de formados por ano
plt.figure(figsize=(12,6))
formados_por_ano.plot(kind='bar')
plt.title('Frequência de Formados por Ano')
plt.xlabel('Ano de Formatura')
plt.ylabel('Número de Formados')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('respostas/1_frequencia_formados_por_ano.png')
print("1) Histograma: 1_frequencia_formados_por_ano.png")

# 2) Quantos alunos desistem do curso por ano?
cancelados = df[df['Status'] == 'Cancelado']
cancelados_por_ano = cancelados['Egresso'].str[:4].value_counts()
# print(cancelados_por_ano)
media_cancelados = cancelados_por_ano.mean()
print(f"2) {media_cancelados:.1f} alunos desistem por ano em média")

# 3) Quais as chances do aluno desistir no primeiro ano?
def calcular_duracao(ingresso_completo, egresso):
    # Extrair data do ingresso (formato: "2005/1 (por Vestibular...)")
    ingresso = ingresso_completo.split()[0]  # Pega só "2005/1"
    
    ano_ing = int(ingresso[:4])
    sem_ing = int(ingresso[-1])
    ano_egr = int(egresso[:4]) 
    sem_egr = int(egresso[-1])
    return (ano_egr - ano_ing) + (sem_egr - sem_ing) * 0.5

df_copy = df.copy()
df_copy['duracao'] = df_copy.apply(lambda x: calcular_duracao(x['Ingresso'], x['Egresso']), axis=1)
primeiro_ano_alunos = df_copy[df_copy['duracao'] <= 1.0]
cancelados_primeiro_ano = primeiro_ano_alunos[primeiro_ano_alunos['Status'] == 'Cancelado']
chance_desistir = len(cancelados_primeiro_ano) / len(primeiro_ano_alunos) * 100
print(f"3) {chance_desistir:.1f}% chance de desistir no primeiro ano")

# 4) Qual o percentual médio de desistência durante os anos?
# Calcular desistência por turma de ingresso
df['ano_ingresso'] = df['Ingresso'].str[:4]
turmas = df['ano_ingresso'].unique()
percentuais_por_turma = []

for turma in sorted(turmas):
    alunos_turma = df[df['ano_ingresso'] == turma]
    cancelados_turma = alunos_turma[alunos_turma['Status'] == 'Cancelado']
    if len(alunos_turma) > 0:
        percentual = len(cancelados_turma) / len(alunos_turma) * 100
        percentuais_por_turma.append(percentual)

media_desistencia = sum(percentuais_por_turma) / len(percentuais_por_turma)
print(f"4) {media_desistencia:.1f}% média de desistência por turma")

# Histograma de desistência por turma
turma_percentuais = {}
for turma in sorted(turmas):
    alunos_turma = df[df['ano_ingresso'] == turma]
    cancelados_turma = alunos_turma[alunos_turma['Status'] == 'Cancelado']
    if len(alunos_turma) > 0:
        percentual = len(cancelados_turma) / len(alunos_turma) * 100
        turma_percentuais[turma] = percentual

plt.figure(figsize=(12,6))
plt.bar(turma_percentuais.keys(), turma_percentuais.values())
plt.title('Percentual de Desistência por Turma de Ingresso')
plt.xlabel('Ano de Ingresso')
plt.ylabel('Percentual de Desistência (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('respostas/4_percentual_desistencia_por_turma.png')
print("4) Histograma: 4_percentual_desistencia_por_turma.png")

# 5) Gráfico de frequência para desistências por duração
cancelados_com_duracao = df_copy[df_copy['Status'] == 'Cancelado']
cancelados_duracao = cancelados_com_duracao['duracao'].value_counts().sort_index()
plt.figure(figsize=(10,6))
cancelados_duracao.plot(kind='bar')
plt.title('Frequência de Desistências por Duração no Curso')
plt.xlabel('Anos no Curso')
plt.ylabel('Número de Desistências')
plt.tight_layout()
plt.savefig('respostas/5_frequencia_desistencias_por_duracao.png')
print("5) 5_frequencia_desistencias_por_duracao.png")

# 6) Tempo mais frequente para conclusão
formados_duracao = formados.copy()
formados_duracao['duracao'] = formados_duracao.apply(lambda x: calcular_duracao(x['Ingresso'], x['Egresso']), axis=1)
tempo_mais_frequente = formados_duracao['duracao'].mode()[0]
print(f"6) {tempo_mais_frequente:.1f} anos é o tempo mais frequente")

# 7) Tempo médio para conclusão com box plot
tempo_medio_formados = formados_duracao['duracao'].mean()
plt.figure(figsize=(10,6))
plt.boxplot(formados_duracao['duracao'])
plt.title('Tempo para Conclusão do Curso')
plt.ylabel('Anos')
plt.tight_layout()
plt.savefig('respostas/7_boxplot_tempo_conclusao.png')
print(f"7) {tempo_medio_formados:.1f} anos em média - 7_boxplot_tempo_conclusao.png")

# 8) Histogramas de desistência
# 8a) Por perfil
plt.figure(figsize=(12,6))
cancelados['Perfil'].value_counts().head(10).plot(kind='bar')
plt.title('Desistências por Perfil')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('respostas/8a_histograma_desistencia_perfil.png')

# 8b) Por ano de ingresso
plt.figure(figsize=(10,6))
cancelados['Ingresso'].str[:4].value_counts().sort_index().plot(kind='bar')
plt.title('Desistências por Ano de Ingresso')
plt.xlabel('Ano de Ingresso')
plt.ylabel('Número de Desistências')
plt.tight_layout()
plt.savefig('respostas/8b_histograma_desistencia_ingresso.png')

# 8c) Por ano de cancelamento (momento do cancelamento)
plt.figure(figsize=(10,6))
cancelados_por_ano_egresso = cancelados['Egresso'].str[:4].value_counts().sort_index()
cancelados_por_ano_egresso.plot(kind='bar')
plt.title('Frequência de Cancelamentos por Ano')
plt.xlabel('Ano do Cancelamento')
plt.ylabel('Número de Cancelamentos')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('respostas/8c_frequencia_cancelamentos_por_ano.png')
print("8) 8a_histograma_desistencia_perfil.png, 8b_histograma_desistencia_ingresso.png e 8c_frequencia_cancelamentos_por_ano.png")


