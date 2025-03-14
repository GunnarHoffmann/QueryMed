import streamlit as st
import requests
import json

def search_aliva_api(medicine_name):
    """Retrieves medicine information from the Aliva API."""

    api_url = f"https://www.aliva.de/fact-finder/proxy/rest/v5/search/aliva_de_live?query={medicine_name}&format=json"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if "hits" in data and len(data["hits"]) > 0:
            first_hit = data["hits"][0]
            product_info = first_hit.get("variantValues", [{}])[0]
            name = product_info.get("produktbezeichnung_shop", "Unbekannt")
            link = product_info.get("link", "Unbekannt")
            if link != "Unbekannt":
                link = f"https://www.aliva.de{link}"

            return {"name": name, "link": link}

        return None  # Return None if no hits are found
    except requests.RequestException as e:
        # Handle or log the error appropriately
        print(f"Error fetching medicine info: {e}")  
        return None


# Streamlit UI
st.title("🔎 Medikamenten-Suche auf aliva.de")

medicine_name = st.text_input("Medikament eingeben:", "Terzolin")

if st.button("🔍 Suchen"):
    with st.spinner("Suche läuft..."):
        result = search_aliva_api(medicine_name)

    if isinstance(result, dict):
        st.success("Erstes Produkt gefunden:")
        st.markdown(f"### {result['name']}")
        st.markdown(f"🔗 [Produktlink]({result['link']})")
    elif isinstance(result, str) and result.startswith("Error"):
        st.error(result)
    else:
        st.warning("Kein Produkt gefunden.")
