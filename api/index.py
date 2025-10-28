from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def safe_first(lst, key=None):
    if lst and len(lst) > 0:
        return lst[0].get(key) if key else lst[0]
    return None
def fetch_truecaller(number):
    TOKEN = "a2i0a--xGEup3VdVkAZ5pEdGVr36IAiYoER_c8qIN5GftDqpn5ENRfvJ17vDX70U"
    url = f"https://search5-noneu.truecaller.com/v2/search?q={number}&countryCode=IN&type=4&encoding=json"
    headers = {
        "User-Agent": "Truecaller/15.32.6 (Android;14)",
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "Authorization": f"Bearer {TOKEN}"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
        info = data.get("data", [{}])[0]

        return {
            "name": info.get("name"),
            "phone": safe_first(info.get("phones"), "e164Format"),
            "carrier": safe_first(info.get("phones"), "carrier"),
            "email": safe_first(info.get("internetAddresses"), "id"),
            "gender": info.get("gender"),
            "city": safe_first(info.get("addresses"), "city"),
            "country": safe_first(info.get("addresses"), "countryCode"),
            "image": info.get("image"),
            "isFraud": info.get("isFraud", False)
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except ValueError as e:
        return {"error": f"Invalid response format: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
@app.route("/truecaller", methods=["GET"])
def truecaller_api():
    number = request.args.get("number")
    if not number:
        return jsonify({"error": "Missing number parameter"}), 400
    result = fetch_truecaller(number)
    return jsonify(result)
nameme__ mainin__":
    app.run(host="0.0.0.0", port=5000, debug=True)