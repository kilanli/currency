from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Döviz türlerini başlangıçta çekelim
def get_currencies():
    response = requests.get("https://api.vatcomply.com/currencies")
    data = json.loads(response.text)
    return list(data.keys())  # ["USD", "EUR", "GBP", ...] gibi

currencies = get_currencies()

@app.route("/", methods=["GET", "POST"])
def index():
    sonuc = None
    if request.method == "POST":
        bozulan_doviz = request.form.get("bozulan_doviz").upper()
        alinan_doviz = request.form.get("alinan_doviz").upper()
        miktar = float(request.form.get("miktar"))

        api_url = f"https://api.vatcomply.com/rates?base={bozulan_doviz}"
        response = requests.get(api_url)
        data = json.loads(response.text)

        kur = data["rates"].get(alinan_doviz)

        if kur:
            alinan_miktar = miktar * kur
            sonuc = f"{miktar} {bozulan_doviz} = {alinan_miktar:.2f} {alinan_doviz}"
        else:
            sonuc = f"{alinan_doviz} kuru bulunamadı."
            
    return render_template("index.html", sonuc=sonuc, currencies=currencies)

if __name__ == "__main__":
    app.run(debug=True)

