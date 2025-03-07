# wcs_1minpeak
# Processamento de Dados de GPS

Este repositório contém um script Python para processar arquivos CSV com dados de GPS de atletas e calcular diferentes métricas de distância percorrida, velocidade e aceleração. O script permite identificar valores máximos acumulados em janelas de 600 linhas para diferentes tipos de análise.

## Funcionalidades
- Carrega automaticamente arquivos CSV de uma pasta específica.
- Extrai o nome do atleta a partir do nome do arquivo.
- Processa diferentes tipos de análise, incluindo:
  - Alta Intensidade (20-25 km/h)
  - Sprint (> 25 km/h)
  - Aceleração (≥ 3 m/s²)
  - Desaceleração (≤ -3 m/s²)
  - Distância total percorrida
- Calcula a distância percorrida entre os instantes e a soma máxima da distância acumulada em janelas de 600 linhas.
- Exporta os resultados para um arquivo Excel.

## Dependências
O script utiliza as seguintes bibliotecas:
- `pandas`
- `os`
- `re`

Certifique-se de instalar as dependências antes de executar o script:
```bash
pip install pandas
```

## Como Usar
1. Defina o caminho da pasta que contém os arquivos CSV no código:
   ```python
   pasta = 'C:/Users/week'
   ```
2. Execute o script para processar os arquivos.
3. O resultado será salvo em um arquivo Excel chamado `resultados_wcs.xlsx` na mesma pasta.

## Estrutura dos Arquivos CSV
Os arquivos CSV devem conter pelo menos 5 colunas, onde:
- A coluna 2 representa a velocidade.
- A coluna 3 representa a aceleração.
- A coluna 4 representa o odômetro.

Os arquivos devem ter um cabeçalho ignorado nas primeiras 8 linhas, e a data do jogo deve estar na primeira linha da nona linha lida.

## Saída
Os resultados serão armazenados em um DataFrame consolidado e salvos no arquivo `resultados_wcs.xlsx`.

## Autor
Este código foi desenvolvido para auxiliar na análise de dados de GPS de atletas, possibilitando uma avaliação detalhada do desempenho físico por Gabriel Colodel para TCC PUCPR2024 e alterado por Vitor Bertoli Nascimento.


