from flask import Flask, request, render_template, redirect
import joblib
import os
import csv
from datetime import datetime

app = Flask(__name__)

# 모델 및 파이프라인 로딩
models = {
    "SVM": joblib.load("pipelines/svm_model.pkl"),
    "DecisionTree": joblib.load("pipelines/decision_tree_model.pkl"),
    "RandomForest": joblib.load("pipelines/random_forest_model.pkl"),
    "GradientBoosting": joblib.load("pipelines/gradient_boost_model.pkl")
}

# 로그 파일 경로
log_path = "logs/prediction_log.csv"
os.makedirs("logs", exist_ok=True)

# 로그 헤더 초기 생성 (처음 한 번)
if not os.path.exists(log_path):
    with open(log_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "model", "input_preview", "prediction", "confidence"])

@app.route("/", methods=["GET", "POST"])
def home():
    result = ''
    if request.method == "POST":
        email_text = request.form.get("email", "").strip()
        model_choice = request.form.get("model")

        if not email_text or not model_choice:
            return render_template("index.html", result="❌ 입력값 또는 모델 선택이 필요합니다.")

        # 선택된 모델 가져오기
        model = models[model_choice]

        # 예측
        prediction = model.predict([email_text])[0]
        try:
            proba = model.predict_proba([email_text])[0]
            confidence = max(proba) * 100
            result = f"예측 결과: {'스팸' if prediction == 1 else '정상 메일'} (신뢰도: {confidence:.2f}%)"
        except:
            confidence = "N/A"
            result = f"예측 결과: {'스팸' if prediction == 1 else '정상 메일'} (확률 없음)"

        # 로그 저장
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([now, model_choice, email_text[:100], prediction, confidence])

    return render_template("index.html", result=result)

@app.route("/logs")
def view_logs():
    logs = []
    if os.path.exists(log_path):
        with open(log_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            logs = list(reader)
    return render_template("logs.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
