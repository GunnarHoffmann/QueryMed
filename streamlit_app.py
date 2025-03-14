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

        # Suche nach Produkten mit der Klasse "product-box"
        products = soup.find_all("div", class_="product-box")

        results = []
        for product in products:
            name_tag = product.find("a", class_="product-title")  # Name des Produkts
            price_tag = product.find("span", class_="product-price")  # Preis des Produkts
            
            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                link = "https://www.aliva.de" + name_tag["href"]
                
                results.append({"name": name, "price": price, "link": link})

        return results if results else None
    except requests.RequestException as e:
        return f"Error: {e}"

# Streamlit UI
st.title("🔎 Medikamenten-Suche auf aliva.de")

medicine_name = st.text_input("Medikament eingeben:", "Terzolin")

if st.button("🔍 Suchen"):
    with st.spinner("Suche läuft..."):
        result = search_aliva(medicine_name)

    if isinstance(result, list):
        st.success(f"{len(result)} Produkte gefunden:")
        for product in result:
            st.markdown(f"- **{product['name']}** - Preis: {product['price']} [Produktlink]({product['link']})")
    elif isinstance(result, str) and result.startswith("Error"):
        st.error(result)
    else:
        st.warning("Keine Produkte gefunden.")




