from flask import Flask, request, jsonify
import video_rating
import re

app = Flask(__name__)

@app.route('/rate', methods=['POST'])
def rate():
    data = request.json
    url = data.get('url', '')
    try:
        video_id = re.findall('v=([A-Za-z0-9_-]+)', url)[0]
        rating = video_rating.get_rating(video_id)
        return jsonify({'rating': round(rating, 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
