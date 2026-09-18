from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

BYPASS_API = "https://api.bypass.vip/bypass"

SUPPORTED_SERVICES = [
    "linkvertise.com", "adf.ly", "exe.io", "exey.io", "ouo.io",
    "adfoc.us", "bc.vc", "shorte.st", "sub2unlock.net", "sub2unlock.com",
    "rekonise.com", "letsboost.net", "mboost.me", "sub4unlock.com",
    "ytsubme.com", "boost.ink", "bit.ly", "cutt.ly", "tinyurl.com",
    "goo.gl", "t.co", "shrto.ml"
]


@app.route("/")
def index():
    return render_template("index.html", services=SUPPORTED_SERVICES)


@app.route("/api/bypass", methods=["POST"])
def api_bypass():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"ok": False, "error": "Vui lòng dán link!"})

    if not url.startswith("http"):
        return jsonify({"ok": False, "error": "URL không hợp lệ!"})

    try:
        payload = {"url": url}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }

        response = requests.post(
            BYPASS_API,
            data=payload,
            headers=headers,
            timeout=60
        )

        if response.status_code == 200:
            try:
                result = response.json()
            except:
                return jsonify({"ok": False, "error": "API trả về dữ liệu không hợp lệ."})

            if result.get("success"):
                return jsonify({
                    "ok": True,
                    "original": result.get("destination", "")
                })
            else:
                return jsonify({
                    "ok": False,
                    "error": result.get("message", "Không thể vượt link này.")
                })
        elif response.status_code == 404:
            return jsonify({"ok": False, "error": "API endpoint không tồn tại (404)."})
        elif response.status_code == 403:
            return jsonify({"ok": False, "error": "API chặn IP (403). Thử lại sau."})
        elif response.status_code == 429:
            return jsonify({"ok": False, "error": "Quá nhiều request (429). Đợi 1 phút."})
        else:
            return jsonify({
                "ok": False,
                "error": "API lỗi " + str(response.status_code)
            })

    except requests.Timeout:
        return jsonify({"ok": False, "error": "API timeout sau 60 giây."})
    except requests.ConnectionError:
        return jsonify({"ok": False, "error": "Không kết nối được API."})
    except Exception as e:
        return jsonify({"ok": False, "error": "Lỗi: " + str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
