import requests
from bs4 import BeautifulSoup
import nltk
import torch
from transformers import BertTokenizer, BertModel

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def process_product_name_with_nlp(product_name):
    # This would use NLP to refine the product search query
    tokens = nltk.word_tokenize(product_name)
    processed_query = " ".join(tokens)  # Simplified example
    return processed_query

#Deep Learning Model Function
def deep_learning_model_inference(product_description):
    # This would use a pre-trained BERT model to analyze the product's description
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    inputs = tokenizer(product_description, return_tensors="pt")
    outputs = model(**inputs)

    # Simplified output to simulate sentiment analysis (not actually performed)
    sentiment_score = torch.sigmoid(outputs.pooler_output.mean()).item()
    return sentiment_score


# Enhanced Web Scraping Function with Dummy NLP and Deep Learning
def get_product_details_with_nlp_and_dl(dummy,product_name, url_template, price_selector, link_prefix=""):
    price, link, sentiment = "Price not found", "Link not found", "N/A"
    processed_product_name = process_product_name_with_nlp(product_name)
    url = url_template.format(processed_product_name.replace(' ', '%20'))

    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        product = soup.find('div', {'class': 'product-desc-rating'})
        if product:
            price = product.find('span', {'class': price_selector}).text.strip()
            link = link_prefix + product.find('a').get('href')
            description = product.find('p', {'class': 'product-desc'}).text  # Assuming there's a description
            sentiment = deep_learning_model_inference(description)  # Fake sentiment analysis score
    except Exception as e:
        print(f"Failed to fetch product details: {e}")
    return price, link, sentiment

def get_snapdeal_details(product_name):
    price, link = "Price not found", "Link not found"
    try:
        url = f"https://www.snapdeal.com/search?keyword={product_name.replace(' ', '%20')}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        product = soup.find('div', {'class': 'product-desc-rating'})
        if product:
            price = product.find('span', {'class': 'lfloat product-price'}).text.strip()
            link = product.find('a').get('href')
    except Exception:
        price, link = "Price not found", "Link not found"
    return price, link

def get_paytmmall_details(product_name):
    price, link = "Price not found", "Link not found"
    try:
        url = f"https://paytmmall.com/shop/search?q={product_name.replace(' ', '%20')}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        product = soup.find('div', {'class': '_3WhJ'})
        if product:
            price = product.find('div', {'class': '_1kMS'}).text.strip()
            link = "https://paytmmall.com" + product.find('a').get('href')
    except Exception:
        price, link = "Price not found", "Link not found"
    return price, link

def get_ebay_details(product_name):
    price, link = "Price not found", "Link not found"
    try:
        url = f"https://www.ebay.com/sch/i.html?_nkw={product_name.replace(' ', '+')}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        product = soup.find('div', {'class': 's-item__info clearfix'})
        if product:
            price = product.find('span', {'class': 's-item__price'}).text
            link = product.find('a', {'class': 's-item__link'}).get('href')
    except Exception:
        price, link = "Price not found", "Link not found"
    return price, link

def get_jiomart_details(product_name):
    price, link = "Price not found", "Link not found"
    try:
        url = f"https://www.jiomart.com/catalogsearch/result?q={product_name.replace(' ', '+')}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        product = soup.find('div', {'class': 'product-detail-wrap'})
        if product:
            price = product.find('span', {'class': 'final-price'}).text.strip().replace('₹', '').strip()
            link = "https://www.jiomart.com" + product.find('a', {'class': 'product-image-photo'}).get('href')
    except Exception:
        price, link = "Price not found", "Link not found"
    return price, link

if __name__ == "__main__":
    product_name = input("Enter the product name: ")
    snapdeal_price, snapdeal_link = get_snapdeal_details(product_name)
    paytmmall_price, paytmmall_link = get_paytmmall_details(product_name)
    ebay_price, ebay_link = get_ebay_details(product_name)
    jiomart_price, jiomart_link = get_jiomart_details(product_name)
    price, link, sentiment = get_product_details_with_nlp_and_dl(product_name,f"https://www.jiomart.com/catalogsearch/result?q={product_name.replace(' ', '+')}",
                                                                 "lfloat product-price")
    print(f"Price for {product_name}: {price}, Product Link: {link}, Sentiment Score: {sentiment}")
    print(f"Snapdeal Price for {product_name}: {snapdeal_price}, Product Link: {snapdeal_link}")
    print(f"Paytm Mall Price for {product_name}: {paytmmall_price}, Product Link: {paytmmall_link}")
    print(f"eBay Price for {product_name}: {ebay_price}, Product Link: {ebay_link}")
    print(f"JioMart Price for {product_name}: {jiomart_price}, Product Link: {jiomart_link}")
