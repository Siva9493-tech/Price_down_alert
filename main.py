import os
import requests
from bs4 import BeautifulSoup
import smtplib
website_address="https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"

# camel camel camel is teh site
# which tells us the whole price history of the current product after pasting the url of the product

G_mail=os.getenv("G_mail")
Y_mail=os.getenv("Y_mail")
G_pass=os.getenv("G_pass")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response=requests.get(website_address,headers=headers)
web_page=response.text

soup=BeautifulSoup(web_page,"html.parser")#web_page.content
price = soup.find(name="span",class_="a-price-whole").get_text()
price_converted=float(price.split(".")[0].replace(",", ""))# as we cannot convert str into float we
#use the replace and from "10,004" by the function is converted into "10004" now for this float is applied and goes on smooth
print(price_converted)

name_of_product=soup.find(name="span",id="productTitle").get_text()
print(name_of_product)

if price_converted< 15000:
    message=f"{name_of_product}{price}\n{website_address}"
    with smtplib.SMTP("smtp.gmail.com",587) as connection:
        connection.starttls()
        connection.login(G_mail,G_pass)
        connection.sendmail(from_addr=G_mail,
            to_addrs=Y_mail,
            msg=f"Subject:Amazon Price Alert!\n\n {message}".encode("utf-8")
        )


