import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr, spearmanr
from scipy.stats import rankdata

# Primeiro exercício

# Dados dos alunos
horas_estudo = [2, 4, 3, 5, 1, 6, 4, 3]
nota_final = [50, 60, 55, 65, 45, 70, 62, 58]
horas_tv = [7, 12, 9, 11, 10, 8, 12, 17]
stress = [8, 6, 7, 5, 9, 4, 6, 7]

dados = [horas_estudo, nota_final, horas_tv, stress]
labels = ['Horas Estudo', 'Nota Final', 'Horas TV', 'Stress']

# 1. Gráficos de dispersão
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

pares = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
for i, (x, y) in enumerate(pares):
    axes[i].scatter(dados[x], dados[y])
    axes[i].set_xlabel(labels[x])
    axes[i].set_ylabel(labels[y])
    r, p = pearsonr(dados[x], dados[y])
    axes[i].set_title(f'r={r:.3f}, p={p:.3f}')

plt.tight_layout()
plt.savefig('exercicio1_correlacao_pearson.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Matriz de correlação
matriz = np.corrcoef(dados)
import pandas as pd
df_corr = pd.DataFrame(matriz, columns=labels, index=labels)
print("\nMatriz de Correlação:")
print(df_corr.round(3))

# 3. Interpretação
def interpretar_correlacao(r, nome):
    if abs(r) >= 0.8: intensidade = "Muito forte"
    elif abs(r) >= 0.6: intensidade = "Forte" 
    elif abs(r) >= 0.4: intensidade = "Moderada"
    elif abs(r) >= 0.2: intensidade = "Fraca"
    else: intensidade = "Muito fraca"
    
    direcao = "positiva" if r > 0 else "negativa"
    return f"{nome}: r={r:.3f} - Correlação {intensidade} {direcao}"

print("\nInterpretação:")
print(interpretar_correlacao(pearsonr(horas_estudo, nota_final)[0], "Horas Estudo × Nota Final"))
print(interpretar_correlacao(pearsonr(horas_estudo, horas_tv)[0], "Horas Estudo × Horas TV"))
print(interpretar_correlacao(pearsonr(horas_estudo, stress)[0], "Horas Estudo × Stress"))
print(interpretar_correlacao(pearsonr(nota_final, stress)[0], "Nota Final × Stress"))

# Segundo exercício

# Dados dos clientes
satisfacao = [5, 4, 3, 2, 1, 4, 5, 3]
compras = [10, 8, 6, 4, 3, 7, 9, 5]
idade = [34, 28, 40, 30, 27, 36, 33, 31]

# 1. Gráficos de dispersão
dados_clientes = [satisfacao, compras, idade]
labels_clientes = ['Satisfação', 'Compras', 'Idade']

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Satisfação × Compras
axes[0].scatter(satisfacao, compras, alpha=0.7, s=100)
axes[0].set_xlabel('Satisfação')
axes[0].set_ylabel('Compras')
rho_sc, p_sc = spearmanr(satisfacao, compras)
axes[0].set_title(f'Satisfação × Compras\nSpearman ρ={rho_sc:.3f}, p={p_sc:.3f}')

# Idade × Compras  
axes[1].scatter(idade, compras, alpha=0.7, s=100, color='orange')
axes[1].set_xlabel('Idade')
axes[1].set_ylabel('Compras')
rho_ic, p_ic = spearmanr(idade, compras)
axes[1].set_title(f'Idade × Compras\nSpearman ρ={rho_ic:.3f}, p={p_ic:.3f}')

plt.tight_layout()
plt.savefig('exercicio2_correlacao_spearman.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Matriz de correlação
matriz_spearman = []
for i in range(len(dados_clientes)):
    linha = []
    for j in range(len(dados_clientes)):
        rho, _ = spearmanr(dados_clientes[i], dados_clientes[j])
        linha.append(rho)
    matriz_spearman.append(linha)

df_spearman = pd.DataFrame(matriz_spearman, columns=labels_clientes, index=labels_clientes)
print("\nMatriz de Correlação (Spearman):")
print(df_spearman.round(3))

# 3. Interpretação
print("\nInterpretação:")
print(interpretar_correlacao(rho_sc, "Satisfação × Compras"))
print(interpretar_correlacao(rho_ic, "Idade × Compras"))
