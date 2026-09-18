from flask import Flask, render_template, request, jsonify
import os
import requests
import re

app = Flask(__name__)

BYPASS_API = "https://api.bypass.vip/"

SUPPORTED_SERVICES = [
    "linkvertise.com",
    "adf.ly",
    "exe.io",
    "exey.io",
    "sub2unlock.net",
    "sub2unlock.com",
    "rekonise.com",
    "letsboost.net",
    "ph.apps2app.com",
    "mboost.me",
    "shortconnect.com",
    "sub4unlock.com",
    "ytsubme.com",
    "bit.ly",
    "social-unlock.com",
    "boost.ink",
    "goo.gl",
    "shrto.ml",
    "t.co",
    "tinyurl.com",
    "shorte.st",
    "bc.vc",
    "ouo.io",
    "adfoc.us",
    "link4m.net",
    "link4m.co",
]


@app.route("/")
def index():
    return render_template("index.html", services=SUPPORTED_SERVICES)


@app.route("/api/bypass", methods=["POST"])
def api_bypass():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"ok": False, "error": "Vui lòng dán link cần vượt!"})

    if not url.startswith("http"):
        return jsonify({"ok": False, "error": "URL không hợp lệ!"})

    try:
        payload = {"url": url}
        response = requests.post(BYPASS_API, data=payload, timeout=30)

        if response.status_code == 200:
            try:
                result = response.json()
            except:
                return jsonify({"ok": False, "error": "API trả về dữ liệu không hợp lệ."})

            if result.get("success"):
                return jsonify({
                    "ok": True,
                    "original": result.get("destination", ""),
                    "status": "success"
                })
            else:
                return jsonify({
                    "ok": False,
                    "error": result.get("message", "Không thể vượt link này.")
                })
        else:
            return jsonify({"ok": False, "error": "API lỗi: " + str(response.status_code)})

    except requests.Timeout:
        return jsonify({"ok": False, "error": "API timeout, thử lại sau."})
    except Exception as e:
        return jsonify({"ok": False, "error": "Lỗi: " + str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
