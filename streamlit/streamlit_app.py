import streamlit as st
import requests

# Configurando o título da aplicação
st.title("Predição de Churn em E-Commerce")

# Criando um formulário para coletar os dados de entrada
with st.form(key='churn_form'):
    col1, col2, col3 = st.columns(3)

    with col1:
        tenure = st.number_input("Anos com a empresa", min_value=0, step=1, value=0)
        city_tier = st.selectbox("City tier", [1, 2, 3])
        warehouse_to_home = st.number_input("Distância fábrica-casa (km)", min_value=0, step=1, value=0)
        hour_spend_on_app = st.number_input("Horas no app/semana", min_value=0)
        number_of_device_registered = st.number_input("Dispositivos registrados", min_value=1)
    
    with col2:
        satisfaction_score = st.slider("Score de Satisfação", min_value=1, max_value=5)
        number_of_address = st.number_input("Endereços cadastrados", min_value=1)
        day_since_last_order = st.number_input("Dias desde último pedido", min_value=0)
        cashback_amount = st.number_input("Cashback", min_value=0.0)
        complain = st.selectbox("Reclamação cadastrada?", ["Não", "Sim"])

    with col3:
        preferred_order_cat = st.selectbox("Categoria preferida", ["Laptop & Accessory", "Mobile Phone", "Outros"])
        marital_status = st.selectbox("Estado Civil", ["Single", "Married", "Outro"])
        preferred_payment_mode = st.selectbox("Pagamento preferido", ["COD", "E wallet", "Debit Card", "Credit Card", "Outro"])
        preferred_login_device = st.selectbox("Login preferido", ["Mobile Phone", "Phone", "Computer", "Outro"])
        gender = st.selectbox("Gênero", ["Male", "Female"])

    submit_button = st.form_submit_button("Enviar")

# Quando o botão é pressionado, faz a chamada para a API
if submit_button:
    input_data = {
        "Tenure": tenure,
        "CityTier": city_tier,
        "WarehouseToHome": warehouse_to_home,
        "HourSpendOnApp": hour_spend_on_app,
        "NumberOfDeviceRegistered": number_of_device_registered,
        "SatisfactionScore": satisfaction_score,
        "NumberOfAddress": number_of_address,
        "DaySinceLastOrder": day_since_last_order,
        "CashbackAmount": cashback_amount,
        "Complain": 0 if complain == "Não" else 1,
        "PreferedOrderCat": preferred_order_cat,
        "MaritalStatus": marital_status,
        "PreferredPaymentMode": preferred_payment_mode,
        "PreferredLoginDevice": preferred_login_device,
        "Gender": gender
    }

    print(input_data)

    # Fazendo a requisição para a API
    # response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
    response = requests.post("http://fastapi-dev:8000/predict", json=input_data)

    if response.status_code == 200:
        result = response.json()
        prob = result['probabilidade']

        st.success(f"Probabilidade de Churn: {prob:.2f}")

        if prob > 0.8:
            st.markdown(
                '<div style="background-color:#ff4d4d;padding:16px;border-radius:8px;color:white;font-weight:bold;font-size:18px">'
                '🚨 Alerta! Cliente altamente tendente ao cancelamento (chance maior que 80%)'
                '</div>', unsafe_allow_html=True)
        elif prob > 0.3:
            st.markdown(
                '<div style="background-color:#ffd700;padding:16px;border-radius:8px;color:#333;font-weight:bold;font-size:18px">'
                '⚠️ Atenção! Cliente pode estar tendente ao cancelamento (chance intermediária, entre 30% e 80%)'
                '</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="background-color:#4CAF50;padding:16px;border-radius:8px;color:white;font-weight:bold;font-size:18px">'
                '✅ Cliente com baixa tendência ao cancelamento'
                '</div>', unsafe_allow_html=True)