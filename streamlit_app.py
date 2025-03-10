import streamlit as st
import requests
import json
from PIL import Image
from io import BytesIO
import os

# Konfiguracja strony
st.set_page_config(
    page_title="AutoIMG", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Stałe wartości - pobieranie klucza API z zmiennych środowiskowych lub bezpośrednio
TEMPLATE_ID = "c4381011-8d4a-42e9-be03-565ff7793ed9"
API_KEY = os.environ.get("ABYSSALE_API_KEY", "sKctkiI0K2W0howzETY9avQPo0sIrRvoe6qCYK60")
API_URL = f"https://api.abyssale.com/banner-builder/{TEMPLATE_ID}/generate"

# Dodanie informacji o bezpieczeństwie
st.sidebar.markdown("## Informacje o API")
st.sidebar.info(
    "Ta aplikacja używa API Abyssale do generowania grafik. "
    "Klucz API jest przechowywany bezpiecznie jako zmienna środowiskowa."
)

# Przykładowa grafika
st.image("https://production-banners.s3-eu-west-1.amazonaws.com/3e56f04a-394c-4460-ae5d-5b6886e4591b/c2f5d16e-cb9d-4cdd-ae54-a52836466a49.jpeg", caption="Przykładowa grafika", width=600)

# Funkcja do wysyłania zapytania do API
def generate_banner(data):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Błąd podczas generowania grafiki: {response.status_code}")
        st.error(response.text)
        return None

# Wyświetlanie wygenerowanej grafiki
def display_banner(response_data):
    if response_data and "file" in response_data and "url" in response_data["file"]:
        image_url = response_data["file"]["url"]
        try:
            image_response = requests.get(image_url)
            image = Image.open(BytesIO(image_response.content))
            st.image(image, caption="Wygenerowana grafika", use_column_width=True)
            
            # Wyświetlanie linku do pobrania
            st.markdown(f"[Pobierz grafikę]({image_url})")
            
            # Wyświetlanie informacji o grafice
            with st.expander("Szczegóły grafiki"):
                st.json(response_data)
        except Exception as e:
            st.error(f"Błąd podczas wyświetlania grafiki: {e}")
    else:
        st.error("Brak danych grafiki w odpowiedzi.")

# Interfejs użytkownika
st.title("Generator Grafik Webinarowych dla Weterynarzy")
st.markdown("Uzupełnij formularz, aby wygenerować grafikę webinarową.")

# Bardziej kompaktowy formularz
st.subheader("Kolory i layout")
col1, col2 = st.columns(2)
with col1:
    background_color = st.color_picker("Kolor tła", "#00215C")
with col2:
    shape_color = st.color_picker("Kolor akcentów", "#5EA3FD")

# Tytuł i podtytuł
st.subheader("Treść główna")
title = st.text_input("Tytuł", "Nowoczesne podejście do leczenia chorób stawów u psów")
subtitle = st.text_input("Data wydarzenia", "Czwartek, 18 marca 2025")

# Prelegenci w dwóch kolumnach
st.subheader("Prelegenci")
col1, col2 = st.columns(2)

# Prelegent 1
with col1:
    st.markdown("**Prelegent 1**")
    company1 = st.text_input("Klinika/instytucja 1", "Klinika Weterynaryjna PetCare")
    role1 = st.text_input("Stanowisko 1", "Specjalista chirurgii weterynaryjnej")
    avatar1_url = st.text_input(
        "URL zdjęcia 1", 
        "https://production-banners.s3-eu-west-1.amazonaws.com/templates/v2/3e56f04a-394c-4460-ae5d-5b6886e4591b/c4381011-8d4a-42e9-be03-565ff7793ed9/v2_6f85af7f-1787-4746-bbe4-2720849f9453.jpeg"
    )
    st.image(avatar1_url, width=100)

# Prelegent 2
with col2:
    st.markdown("**Prelegent 2**")
    company2 = st.text_input("Klinika/instytucja 2", "Uniwersytet Przyrodniczy")
    role2 = st.text_input("Stanowisko 2", "Profesor nauk weterynaryjnych")
    avatar2_url = st.text_input(
        "URL zdjęcia 2", 
        "https://production-banners.s3-eu-west-1.amazonaws.com/templates/v2/3e56f04a-394c-4460-ae5d-5b6886e4591b/c4381011-8d4a-42e9-be03-565ff7793ed9/v2_8bc2ee86-0068-462a-82d1-9ff57c7d4081.jpeg"
    )
    st.image(avatar2_url, width=100)

# Logo
st.subheader("Logo")
logo_url = st.text_input(
    "URL logo", 
    "https://www.animal-expert.pl/media/cache/logo_175_73/uploads/665/5e1/6655e1a0adad2553433357.svg?extension=jpg&version=844"
)
st.image(logo_url, width=200)

# Przycisk generowania
if st.button("Generuj grafikę", type="primary"):
    with st.spinner("Generowanie grafiki..."):
        # Przygotowanie danych do wysłania
        data = {
            "template_format_name": "facebook-post",
            "elements": {
                "root": {
                    "background_color": background_color
                },
                "shape_2": {
                    "background_color": shape_color,
                    "hidden": False
                },
                "shape_1": {
                    "background_color": shape_color,
                    "hidden": False
                },
                "shape_0": {
                    "background_color": shape_color,
                    "hidden": False
                },
                "text_company2": {
                    "payload": company2,
                    "color": shape_color,
                    "font_size": 38,
                    "font": "61569992-33c5-11ea-9877-92672c1b8195",
                    "font_weight": 700,
                    "line_height": 130,
                    "alignment": "middle center",
                    "hidden": False
                },
                "text_avatar2": {
                    "payload": role2,
                    "color": "#FFFFFF",
                    "font_size": 38,
                    "font": "61569992-33c5-11ea-9877-92672c1b8195",
                    "font_weight": 700,
                    "line_height": 130,
                    "alignment": "middle center",
                    "hidden": False
                },
                "image_avatar2": {
                    "image_url": avatar2_url,
                    "fitting_type": "cover",
                    "alignment": "middle center",
                    "mask_name": "circle",
                    "filter_name": "grayscale",
                    "hidden": False
                },
                "text_company1": {
                    "payload": company1,
                    "color": shape_color,
                    "font_size": 38,
                    "font": "61569992-33c5-11ea-9877-92672c1b8195",
                    "font_weight": 700,
                    "line_height": 130,
                    "alignment": "middle center",
                    "hidden": False
                },
                "text_role1": {
                    "payload": role1,
                    "color": "#FFFFFF",
                    "font_size": 38,
                    "font": "61569992-33c5-11ea-9877-92672c1b8195",
                    "font_weight": 700,
                    "line_height": 130,
                    "alignment": "top center",
                    "hidden": False
                },
                "image_avatar1": {
                    "image_url": avatar1_url,
                    "fitting_type": "cover",
                    "alignment": "middle center",
                    "mask_name": "circle",
                    "filter_name": "grayscale",
                    "hidden": False
                },
                "text_subtitle": {
                    "payload": subtitle,
                    "color": "#FFFFFF",
                    "font_size": 45,
                    "font": "61569992-33c5-11ea-9877-92672c1b8195",
                    "font_weight": 600,
                    "line_height": 130,
                    "alignment": "top center",
                    "hidden": False
                },
                "text_title": {
                    "payload": title,
                    "color": "#FFFFFF",
                    "font_size": 60,
                    "font": "61569992-33c5-11ea-9877-92672c1b8195",
                    "font_weight": 700,
                    "line_height": 100,
                    "alignment": "top center",
                    "hidden": False
                },
                "logo_vektor": {
                    "image_url": logo_url,
                    "alignment": "middle center",
                    "hidden": False
                }
            }
        }
        
        # Wyświetlenie przygotowanych danych (opcjonalnie)
        with st.expander("Dane wysyłane do API"):
            st.json(data)
        
        # Wysłanie zapytania do API
        response_data = generate_banner(data)
        
        # Wyświetlenie wygenerowanej grafiki
        if response_data:
            display_banner(response_data)