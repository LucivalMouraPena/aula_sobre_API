import requests
import calendar
import matplotlib.pyplot as plt 
from datetime import datetime

# --- Primeiro Bloco (Cotação Atual) ---
url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL'
response = requests.get(url)
cotacoes = response.json()

print("--- Cotações Atuais ---")
print(cotacoes)
print("-" * 30)

# --- Segundo Bloco (Histórico de BTC de Janeiro a Junho de 2026) ---
print("\nBuscando histórico de Bitcoin de Janeiro a Junho de 2026...")

cotacoes_btc = {}
ano_atual = 2026
hoje = datetime.now()

for mes in range(1, 7):
    # Se for o mês atual, limitamos a busca até o dia de hoje para a API não falhar
    if mes == hoje.month and ano_atual == hoje.year:
        ultimo_dia = hoje.day
    else:
        _, ultimo_dia = calendar.monthrange(ano_atual, mes)
    
    start_date = f"{ano_atual}{mes:02d}01"
    end_date = f"{ano_atual}{mes:02d}{ultimo_dia:02d}"
    
    # 1000 é um limite seguro para garantir que todos os dias retornem
    url_btc = f'https://economia.awesomeapi.com.br/json/daily/BTC-BRL/1000?start_date={start_date}&end_date={end_date}'
    
    response_btc = requests.get(url_btc)
    
    if response_btc.status_code == 200:
        dados_mes = response_btc.json()
        # Garante que só salvamos se a API realmente retornou uma lista de dados válida
        if isinstance(dados_mes, list) and len(dados_mes) > 0:
            cotacoes_btc[mes] = dados_mes
            print(f"Mês {mes:02d}/2026: {len(dados_mes)} registros obtidos.")
        else:
            print(f"Mês {mes:02d}/2026: Nenhum registro disponível ainda.")
    else:
        print(f"Erro ao buscar dados do mês {mes:02d} (Status: {response_btc.status_code})")

print("\n--- Resultados Finais ---")
print('A quantidade de meses salvos no dicionário:', len(cotacoes_btc))



''' Outro grafico com mais detalhes, na cor chocolate co cenoura ouro, caso queira visualizar
o preço de fechamento diário
do Bitcoin de Janeiro a Junho de 2026:'''

# --- Terceiro Bloco (Gráfico com Tempero de Designer) ---
medias_mensais = []
meses_eixo_x = []

for mes in sorted(cotacoes_btc.keys()):
    dados = cotacoes_btc[mes]
    valores_dia = []
    for dia in dados:
        if 'bid' in dia:
            valores_dia.append(float(dia['bid']))
            
    if valores_dia:
        media_mes = sum(valores_dia) / len(valores_dia)
        medias_mensais.append(media_mes)
        meses_eixo_x.append(mes)

if meses_eixo_x and meses_eixo_x[0] > meses_eixo_x[-1]:
    meses_eixo_x.reverse()
    medias_mensais.reverse()

if medias_mensais:
    # --- PALETA DE CORES (DESIGNER) ---
    COR_FUNDO = '#121214'       # Cinza quase preto moderno
    COR_LINHA = '#F7931A'       # Laranja oficial do Bitcoin
    COR_TEXTO = '#E1E1E6'       # Branco fosco elegante
    COR_GRADE = '#29292E'       # Grade sutil
    
    # Criar a figura com o fundo escuro
    fig, ax = plt.subplots(figsize=(11, 6), facecolor=COR_FUNDO)
    ax.set_facecolor(COR_FUNDO)

    # 1. Plotar a linha principal com espessura e suavidade
    ax.plot(meses_eixo_x, medias_mensais, color=COR_LINHA, linewidth=3, 
            marker='o', markersize=8, markerfacecolor=COR_FUNDO, markeredgewidth=2,
            label="Preço Médio Mensal")

    # 2. Efeito "Glow" (Preenchimento suave abaixo da linha)
    ax.fill_between(meses_eixo_x, medias_mensais, color=COR_LINHA, alpha=0.15)

    # 3. Customização dos Eixos e Títulos
    ax.set_title('Evolução do Preço Médio do Bitcoin (BTC-BRL)', 
                 fontsize=16, fontweight='bold', color=COR_TEXTO, pad=20)
    ax.set_xlabel('Meses de 2026', fontsize=11, color=COR_TEXTO, labelpad=12)
    ax.set_ylabel('Preço Médio (R$)', fontsize=11, color=COR_TEXTO, labelpad=12)

    # 4. Ajustar os limites e nomes dos meses no eixo X
    nomes_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    ax.set_xticks(meses_eixo_x)
    ax.set_xticklabels(nomes_meses, fontsize=10, color=COR_TEXTO)

    # Formatar valores do eixo Y para moeda (R$) de forma limpa
    valores_y = ax.get_yticks()
    ax.set_yticklabels([f"R$ {val/1000:.0f}k" for val in valores_y], fontsize=10, color=COR_TEXTO)

    # 5. Grade sutil e moderna
    ax.grid(True, linestyle=':', color=COR_GRADE, alpha=0.7)

    # 6. Remover as bordas superiores e direitas da caixa (Spines)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_color(COR_GRADE)

    # 7. Legenda minimalista
    legend = ax.legend(facecolor=COR_FUNDO, edgecolor=COR_GRADE, loc='upper left')
    for text in legend.get_texts():
        text.set_color(COR_TEXTO)

    plt.tight_layout()
    plt.show()
else:
    print("Não há dados suficientes para gerar o gráfico.")