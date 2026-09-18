from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# ENDPOINT ĐÚNG (đã fix 404)
BYPASS_API = "https://api.bypass.vip/bypass"

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
        # Gửi form-data (KHÔNG phải JSON) - đây là fix chính
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

        # Log để debug
        print("=" * 50)
        print("URL gui:", url)
        print("Status:", response.status_code)
        print("Response:", response.text[:300])
        print("=" * 50)

        if response.status_code == 200:
            try:
                result = response.json()
            except Exception as e:
                return jsonify({
                    "ok": False,
                    "error": "API trả về không phải JSON: " + response.text[:100]
                })

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
            return jsonify({
                "ok": False,
                "error": "API endpoint không tồn tại (404). Có thể API đã đổi."
            })
        elif response.status_code == 403:
            return jsonify({
                "ok": False,
                "error": "API chặn IP (403). Thử lại sau hoặc dùng VPN."
            })
        elif response.status_code == 429:
            return jsonify({
                "ok": False,
                "error": "Quá nhiều request (429). Đợi 1 phút rồi thử lại."
            })
        else:
            return jsonify({
                "ok": False,
                "error": "API lỗi " + str(response.status_code) + ": " + response.text[:100]
            })

    except requests.Timeout:
        return jsonify({"ok": False, "error": "API timeout sau 60 giây. Thử lại."})
    except requests.ConnectionError:
        return jsonify({"ok": False, "error": "Không kết nối được tới API. Kiểm tra mạng."})
    except Exception as e:
        return jsonify({"ok": False, "error": "Lỗi: " + str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
