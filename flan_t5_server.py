import sys
from flask import Flask, request, Response
from flask_cors import CORS
from transformers import T5Tokenizer, T5ForConditionalGeneration


def init_model(_model_name):
    _tokenizer = T5Tokenizer.from_pretrained(_model_name)
    _model = T5ForConditionalGeneration.from_pretrained(_model_name, device_map="auto")
    return _tokenizer, _model


def run_model(text, max_tokens):
    input_ids = tokenizer(text, return_tensors="pt").input_ids.to(model.device)

    outputs = model.generate(input_ids, max_new_tokens=max_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
def prompt():
    max_tokens = 200
    if "max_tokens" in request.form:
        max_tokens = int(request.form["max_tokens"])
    text = request.form["text"]
    answer = run_model(text=text, max_tokens=max_tokens)
    return Response(answer, content_type='text/plain; charset=utf-8')


if __name__ == "__main__":
    match sys.argv[2]:
        case "run":
            model_name = sys.argv[1]
            print("initializing models and starting up ...")
            print(f"model name: {model_name}")
            tokenizer, model = init_model(model_name)
            app.run(host="0.0.0.0")
        case "init":
            model_name = sys.argv[1]
            print("initializing models and exiting ...")
            print(f"model name: {model_name}")
            tokenizer, model = init_model(model_name)
        case _:
            print("unknown command")
