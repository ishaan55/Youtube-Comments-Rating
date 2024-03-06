from flask import Flask, render_template, request
import video_rating
import re

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        print("Button pressed")
        url = request.form.get('url')
        video_id = re.findall('v=([A-Za-z0-9_-]+)', url)[0]
        rating = video_rating.get_rating(video_id)
        return render_template('base.html', rating=round(rating, 2))

    return render_template('base.html')

if __name__ == '__main__':
    app.run()
