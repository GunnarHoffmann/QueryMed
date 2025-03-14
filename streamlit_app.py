import streamlit as st
import requests
from bs4 import BeautifulSoup

def search_medicine(medicine_name):
    """Search for a medicine on Shop-Apotheke.de and return the product link if found."""
    search_url = f"https://www.shop-apotheke.com/search.htm?query={medicine_name}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the first product link
        product = soup.find("a", class_="product-card-cta")  # Adjust class if needed

        if product:
            product_link = "https://www.shop-apotheke.com" + product["href"]
            return product_link
        else:
            return None  # No product found
    except requests.RequestException as e:
        return f"Error: {e}"

# Streamlit UI
st.title("Medicine Availability Checker")

# Default value
medicine_name = st.text_input("Enter medicine name:", "Terzolin")

if st.button("Search"):
    with st.spinner("Searching..."):
        result = search_medicine(medicine_name)

    if isinstance(result, str) and result.startswith("https://"):
        st.success(f"Medicine found! [Click here]({result}) to view on Shop-Apotheke.de")
    elif isinstance(result, str) and result.startswith("Error"):
        st.error(result)
    else:
        st.warning("Medicine not found on Shop-Apotheke.de.")
