from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Инициализация модели и токенизатора
model_name = "Qwen/Qwen2.5-Coder-32B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", trust_remote_code=True)

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    # Токенизация и генерация ответа
    inputs = tokenizer(user_input, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
    outputs = model.generate(inputs.input_ids, max_length=512, do_sample=True, temperature=0.7)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
