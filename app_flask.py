from flask import Flask, request
app = Flask(__name__)
@app.route("/currency", methods=["GET"])
def currency():
    today = "today" in request.args
    key = request.args.get("key")
    result = "USD - 41,5"
    if today:
      result += "(today)"
    if key:
        result += f"|key = {key}"
    return result

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
