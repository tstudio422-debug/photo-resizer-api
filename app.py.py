from flask import Flask, request, send_file, jsonify
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/resize', methods=['POST'])
def resize_image():
    file = request.files['image']
    target_kb = int(request.form.get('target_kb', 50)) # डिफॉल्ट 50kb
    
    img = Image.open(file.stream)
    img = img.convert("RGB") # JPG के लिए सुरक्षित
    
    # इमेज को कंप्रेस करने का लॉजिक (Loop)
    quality = 95
    output = io.BytesIO()
    
    while quality > 5:
        output.seek(0)
        output.truncate(0)
        img.save(output, format="JPEG", quality=quality)
        if output.tell() / 1024 <= target_kb:
            break
        quality -= 5
    
    output.seek(0)
    return send_file(output, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True) 