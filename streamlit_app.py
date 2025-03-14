import streamlit as st
import requests
import json

def search_aliva_api(medicine_name):
    api_url = f"https://www.aliva.de/fact-finder/proxy/rest/v5/search/aliva_de_live?query={medicine_name}&format=json"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if "hits" in data and len(data["hits"]) > 0:
            first_hit = data["hits"][0]
            product_info = first_hit.get("variantValues", [{}])[0]
            name = product_info.get("produktbezeichnung_shop", "Unbekannt")
            pzn = product_info.get("pzn", "Keine PZN")
            link = f"https://www.aliva.de/p/{pzn}" if pzn != "Keine PZN" else "https://www.aliva.de"
            
            return {"name": name, "link": link}
        
        return None
    except requests.RequestException as e:
        return f"Error: {e}"

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




