from flask  import Flask , render_template ,request
import joblib
import backend

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict",methods=["POST"])
def predict():
    data = {
        "Maths_Marks" : float(request.form["Maths"]),
        "Physics_Marks" : float(request.form["Physics"]),
        "Chemistry_Marks" : float(request.form["Chemistry"]),
        "Shift_Difficulty" : request.form["Paper Difficulty"]
    }

    result = backend.predict(data)

    return render_template(
        "result.html",
        Rank=round(result["Rank"],2),
        Percentile=round(result["Percentile"],2)
    )

if __name__ == "__main__":
    app.run(debug=True)
