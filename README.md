# PD-redes-neurais-tensorflow

### como rodar o ambiente

1. crie um ambiente com Python 3.11. Exemplo:
```conda create --name PD_env_redes_neurais python=3.11 --no-default-packages -y```
```conda activate PD_env_redes_neurais```

2. Rode:
```pip install -r requirements.txt``` 

### como foi gerado o environment deste projeto
1. criei manualmente o requirements.in
2. rodei:
```conda create --name PD_env_redes_neurais python=3.11 --no-default-packages -y```
```conda activate PD_env_redes_neurais```
```python -m pip install pip-tools ```
```pip-compile```
- este último comando vai preencher o requirements.txt a partir do requirements.in
3. rodei:
```pip install -r requirements.txt``` 
- este último comando vai instalar as dependências do projeto a partir do requirements.txt

--------------------
## SUBINDO EM CONTAINER
### rodando em container
```docker compose up```


--------------------
## SUBINDO DE FORMA LOCAL
### rodando a API de forma local

```cd fastapi```
```uvicorn main:app --reload```


### consumindo a API via Streamlit de forma local
ajuste a url para onde aponta a aplicação streamlit para http://127.0.0.1:8000
```
streamlit run streamlit/streamlit_app.py
```

---------------------
### documentação da API
Acessar http://127.0.0.1:8000/docs

### Streamlit
Acessar http://localhost:8501/