import streamlit as st
import requests
from bs4 import BeautifulSoup

def search_aliva(medicine_name):
    search_url = f"https://www.aliva.de/search?query={medicine_name}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Produkte auf der Ergebnisseite suchen
        products = soup.find_all("a", class_="product__link")

        results = []
        for product in products:
            name = product.get_text(strip=True)
            link = "https://www.aliva.de" + product["href"]
            results.append({"name": name, "link": link})

        return results if results else None
    except requests.RequestException as e:
        return f"Error: {e}"

# Streamlit UI
st.title("🔎 Medikamentencheck auf aliva.de")

medicine_name = st.text_input("Medikament eingeben:", "Terzolin")

if st.button("🔍 Suchen"):
    with st.spinner("Suche auf aliva.de läuft..."):
        result = search_aliva(medicine_name)

    if isinstance(result, list):
        st.success(f"{len(result)} Produkte gefunden:")
        for product in result:
            st.markdown(f"- [{product['name']}]({product['link']})")
    elif isinstance(result, str) and result.startswith("Error"):
        st.error(result)
    else:
        st.warning("Keine Produkte gefunden.")


