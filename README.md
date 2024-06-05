# Reprocessamento de Notas

Este é um projeto que permite o reprocessamento de notas por período ou por ID de proprietário (Owner ID). Ele inclui uma interface gráfica simples usando Tkinter para entrada de dados e interação com o usuário.

## Requisitos

- Python 3.x
- Bibliotecas:
  - tkinter
  - requests
  - openpyxl

## Funcionalidades

- **Envio por Período:** Permite ao usuário enviar notas dentro de um intervalo de datas especificado.
- **Envio por ID:** Permite ao usuário enviar notas com base em um arquivo contendo IDs de proprietários.

## Instalação

1. Clone o repositório:

git clone https://github.com/seu_usuario/nome_do_repositorio.git

2. Navegue até o diretório do projeto: 

cd nome_do_repositorio

3. Instale as dependências: 

pip install -r requirements.txt

4. Execute o aplicativo:

python main.py


## Uso

1. Ao iniciar o aplicativo, insira o ID do proprietário (Owner ID) na caixa de entrada fornecida.
2. Selecione uma das opções:
   - **Enviar por Período:** Insira as datas inicial e final no formato AAAA-MM-DD e clique em "Enviar por Período".
   - **Enviar por ID:** Selecione um arquivo contendo os IDs de proprietários e clique em "Enviar por ID".

## Arquivos

- **config.py:** Arquivo de configuração com constantes para o URL do endpoint, número máximo de tentativas e atraso entre tentativas.
- **file_manager.py:** Módulo para gerenciar a criação e manipulação de arquivos, incluindo a escrita de registros de sucesso e erro.
- **logger.py:** Módulo para registrar mensagens de log em um arquivo de texto.
- **request_manager.py:** Módulo principal que lida com as solicitações para enviar notas por período ou ID do proprietário.
- **main.py:** Arquivo principal que contém a interface gráfica e interação com o usuário usando Tkinter.
