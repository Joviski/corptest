import io

import pandas as pd

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from flask_restful import Api
from utils.create_histogram import create_color_histogram
from utils.create_tsne_visual import create_tsne_visualization

app = Flask(__name__)
api = Api(app)
CORS(
    app,
    resources={r"*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"], "allow_headers": ["Content-Type", "Authorization"]}},
    expose_headers=["Content-Disposition"]
)


@app.route('/analyze' , methods=['POST'])
def analyze():
    if request.is_json:
        return jsonify({"message": "Unsupported content type"}), 400
    
    input_file = request.files.get("file")
    if not input_file:
        return jsonify({"message": "Invalid Payload"}), 400
    
    if input_file.filename.endswith(".csv"):
        file_content = input_file.stream.read().decode('utf-8')

        string_io = io.StringIO(file_content)
        
        df = pd.read_csv(string_io)
        response_dict = {}
        for header in df.columns:
            try:
                mean_value = df[header].mean()
                median_value = df[header].median()
                mode_value = df[header].mode().to_list()
                quartiles_value = df[header].quantile([0.25, 0.5, 0.75]).to_dict()
                response_dict[str(header)] = {
                    "mean": mean_value,
                    "median": median_value,
                    "mode": mode_value,
                    "quartiles": quartiles_value
                }                
            except TypeError:
                continue
        
        return jsonify(response_dict), 200
    
    elif any(input_file.filename.endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
        rgb_histogram = create_color_histogram(input_file.read())
        return send_file(
            io.BytesIO(rgb_histogram),
            download_name="histogram_" + input_file.filename,
            mimetype=input_file.mimetype,
            as_attachment=True,
        )
    
    elif input_file.filename.endswith(".txt"):
        tsne_visual_bytes = create_tsne_visualization(input_file.read().decode("utf-8"))
        return send_file(
            tsne_visual_bytes,
            download_name="tsne_visual_" + input_file.filename.split(".")[0] + ".png",
            mimetype="image/png",
            as_attachment=True,
        )

    return jsonify({"message": "Invalid File Type"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)