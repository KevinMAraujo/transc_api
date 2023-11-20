## Docs

### Instalação
1. Crie o ambiente virtual:  
   * `pip install virtualenv` ou  `python pip install virtualenv` 
   * `python -m venv app_venv`
2. Ative o ambiente virtual:
   * `app_venv\Scripts\activate` ou `app_venv\Scripts\activate.bat`  
3. Instale as bibliotecas - `pip install -r requirements.txt`
4. Execute o arquivo `main.py` com o comando - `uvicorn main:app --reload`
5. Abre o link no navegador `http://127.0.0.1:8000/`
6. Abra o link `http://127.0.0.1:8000/docs` para visualizar as rotas
