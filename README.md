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

### rodando a API
```cd src```
```uvicorn main:app --reload```

### documentação da API
Acessar http://127.0.0.1:8000/docs


### consumindo a API via Streamlit
```
streamlit run streamlit-churn-app/src/streamlit_app.py
```