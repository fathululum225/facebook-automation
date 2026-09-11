from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automation Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 50px auto;
            padding: 20px;
        }

        .card {
            padding: 25px;
            border: 1px solid #ddd;
            border-radius: 12px;
        }

        input {
            width: 100%;
            padding: 12px;
            margin: 8px 0 16px;
            box-sizing: border-box;
        }

        button {
            padding: 12px 20px;
            cursor: pointer;
        }
    </style>
</head>
<body>

<div class="card">
    <h1>Automation Dashboard</h1>

    <label>Target URL</label>
    <input type="url" placeholder="https://contoh.com/...">

    <label>Jumlah proses</label>
    <input type="number" value="1" min="1">

    <button type="button">
        Jalankan
    </button>
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)