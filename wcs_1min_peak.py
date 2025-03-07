import pandas as pd
import os
import re

# Definir o caminho da pasta contendo os arquivos CSV
pasta = 'C:/Users/Semana 48'

# Obter a lista de arquivos CSV na pasta
arquivos_csv = [f for f in os.listdir(pasta) if f.endswith('.csv')]

# Função para extrair o nome do atleta do nome do arquivo
def extrair_nome_atleta(arquivo):
    match = re.search(r'for\s([\w\s]+)\s', arquivo)
    if match:
        nome = match.group(1).strip().split()[0]  # Pega o primeiro nome
        return nome
    return "Desconhecido"

# Função para processar os dados
def processar_dados(arquivos_csv, tipo, pasta):
    resultados = {}

    for arquivo in arquivos_csv:
        caminho_arquivo = os.path.join(pasta, arquivo)

        try:
            # Carregar os dados do arquivo CSV (ignorando as 8 primeiras linhas)
            data = pd.read_csv(caminho_arquivo, delimiter=';', skiprows=8, header=None)

            # Extrair a data do jogo da primeira linha da primeira coluna
            data_jogo = pd.read_csv(caminho_arquivo, delimiter=';', skiprows=9, header=None).iloc[0, 0]
            data_jogo = data_jogo.split()[0]  # Extrair apenas a data

            # Verificar se as colunas necessárias existem
            if data.shape[1] < 5:
                raise ValueError(f"O arquivo {arquivo} não possui colunas suficientes. Esperado pelo menos 5 colunas.")

            # Verificar se as colunas contêm valores numéricos válidos
            try:
                if tipo in ['Alta Intensidade', 'Sprint']:
                    data[2] = pd.to_numeric(data[2].str.replace(',', '.'), errors='coerce').fillna(0)  # Velocidade
                data[3] = pd.to_numeric(data[3].str.replace(',', '.'), errors='coerce').fillna(0)  # Aceleração
                data[4] = pd.to_numeric(data[4].str.replace(',', '.'), errors='coerce').fillna(0)  # Odômetro
            except Exception as e:
                raise ValueError(f"Erro ao processar as colunas no arquivo {arquivo}: {e}")

            # Calcular a distância percorrida entre os instantes
            data['distance'] = data[4] - data[4].shift(1)
            data['distance'] = data['distance'].fillna(0)

            # Calcular a distância total percorrida
            total_distance = data['distance'].sum()

            # Criar a coluna de distância acumulada com base no tipo de análise
            if tipo == 'Alta Intensidade':
                data['valid_distance'] = data['distance'].where((data[2] > 20) & (data[2] < 25), 0)
            elif tipo == 'Sprint':
                data['valid_distance'] = data['distance'].where(data[2] > 25, 0)
            elif tipo == 'Aceleração':
                data['valid_distance'] = data['distance'].where(data[3] >= 3, 0)
            elif tipo == 'Desaceleração':
                data['valid_distance'] = data['distance'].where(data[3] <= -3, 0)
            elif tipo == 'Distancia percorrida':
                data['valid_distance'] = data['distance']

            # Calcular a soma da distância acumulada em janelas de 600 linhas
            rolling_distance = data['valid_distance'].rolling(window=600).sum()

            # Identificar a soma máxima da distância acumulada
            max_distance = rolling_distance.max()

            # Extrair o nome do atleta
            nome_atleta = extrair_nome_atleta(arquivo)

            # Armazenar o resultado, usando o arquivo como chave
            if arquivo not in resultados:
                resultados[arquivo] = {'Nome': nome_atleta, 'Data': data_jogo, 'Distancia Total': total_distance}
            resultados[arquivo][tipo] = max_distance

        except Exception as e:
            print(f"Erro ao processar o arquivo {arquivo}: {e}")

    # Retornar os resultados como DataFrame
    return pd.DataFrame.from_dict(resultados, orient='index')

# Criar um DataFrame para acumular todos os resultados
todos_resultados = pd.DataFrame()

# Executar todas as análises e combinar os resultados
for tipo in ['Alta Intensidade', 'Sprint', 'Aceleração', 'Desaceleração', 'Distancia percorrida']:
    resultados_df = processar_dados(arquivos_csv, tipo, pasta)
    todos_resultados = pd.concat([todos_resultados, resultados_df], axis=1)

# Remover duplicatas de colunas desnecessárias
todos_resultados = todos_resultados.loc[:, ~todos_resultados.columns.duplicated()]

# Salvar todos os resultados  Excel
resultado_excel = os.path.join(pasta, 'resultados_wcs.xlsx')
todos_resultados.to_excel(resultado_excel, index=False)

print(f"Resultados salvos em {resultado_excel}")
