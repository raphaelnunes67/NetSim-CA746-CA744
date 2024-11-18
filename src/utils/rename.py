import os

# Caminho da pasta
caminho_pasta = "../data/residential_loadshapes"

# Dicionário de substituições
substituicoes = {
    "Tipo": "Type",
    "SE": "WE",
    "DO": "SU"
}

# Função para renomear os arquivos
def renomear_arquivos(caminho_pasta, substituicoes):
    for nome_arquivo in os.listdir(caminho_pasta):
        novo_nome = nome_arquivo
        for antigo, novo in substituicoes.items():
            novo_nome = novo_nome.replace(antigo, novo)
        # Renomeia o arquivo
        os.rename(os.path.join(caminho_pasta, nome_arquivo), os.path.join(caminho_pasta, novo_nome))
        print(f'Renomeado: {nome_arquivo} -> {novo_nome}')

# Executa a função
renomear_arquivos(caminho_pasta, substituicoes)