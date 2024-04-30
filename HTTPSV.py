from flask import Flask, send_file, request, jsonify, render_template
from PIL import Image
import cv2
import numpy as np
import os

app = Flask(__name__)

# 設定上傳檔案的路徑
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 將路由改寫為 RESTful API 形式
@app.route('/api/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 將上傳的檔案存儲到伺服器
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    # 處理影像
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 將處理後的影像保存到伺服器
    processed_filename = os.path.join(UPLOAD_FOLDER, 'processed_' + file.filename)
    cv2.imwrite(processed_filename, gray)

    # 返回處理後的影像路徑
    return jsonify({'processed_image': processed_filename}), 200

@app.route("/up")
def sendhtml2():
    return render_template("upfile.html")

@app.route("/upfile", methods=['POST'])
def upup():
    if request.method=='POST':
        file=request.files['file']
        # ** convert file to opencv-image **
        pimg = Image.open(file)
        vimg = np.array(pimg)
        
        # ** RGB to BGR **
        vimg = cv2.cvtColor(vimg, cv2.COLOR_RGB2BGR)
        # ** BGR to RGB **
        gray = cv2.cvtColor(vimg, cv2.COLOR_RGB2GRAY)
        
        # **SAVE TO FILE **
        cv2.imwrite(file.filename, gray)
    return send_file(file.filename, mimetype="image/png")

@app.route("/crop")
def sendhtmlcrop():
    return render_template("upfile2.html")

@app.route("/upfile2", methods=['POST'])
def crop():
    if request.method == 'POST':
        file = request.files['file']
        # ** convert file to opencv-image **
        cimg = Image.open(file)
        crimg = np.array(cimg)
                
        # ** left, right **
        x_l, x_r = 500, 1500
        # ** up, down **
        y_u, y_d = 500, 1500 
        # ** crop image **
        crop = crimg[y_u:y_d, x_l:x_r]  # first y, then x
        # Save the cropped image to a file
        cropped_filename = "cropped_image.png"
        cv2.imwrite(cropped_filename, crop)
        
    return send_file(cropped_filename, mimetype="image/png")

@app.route("/resize")
def sendhtmlresize():
    return render_template("upfile4.html")

@app.route("/upfile4", methods=['POST'])
def rese():
    if request.method == 'POST':
        file = request.files['file']
        print(f"File uploaded: {file.filename}")
        # ** convert file to opencv-image **
        cimg = Image.open(file)
        crimg = np.array(cimg)
        
        scale_percent = 200 # 要放大縮小幾%
        width, height = cimg.size  # 使用 cimg.size 獲取圖像寬度和高度
        width = int(width * scale_percent / 100) # 縮放後圖片寬度
        height = int(height * scale_percent / 100) # 縮放後圖片高度
        dim = (width, height) # 圖片形狀 
        
        resize = cv2.resize(crimg, dim, interpolation=cv2.INTER_AREA)  
        rese_filename = "rese_image.png"
        cv2.imwrite(rese_filename, resize)
        
    return send_file(rese_filename, mimetype="image/png")

@app.route("/flip")
def sendhtmlfilp():
    return render_template("upfile5.html")

@app.route("/upfile5", methods=['POST'])
def flipp():
    if request.method == 'POST':
        file = request.files['file']
        print(f"File uploaded: {file.filename}")
        # ** convert file to opencv-image **
        cimg = Image.open(file)
        crimg = np.array(cimg)
        
        output = cv2.flip(crimg, 0)  #上下翻轉
        flip_filename = "flip_image.png"
        cv2.imwrite(flip_filename, output)
        
    return send_file(flip_filename, mimetype="image/png")

@app.route("/flip2")
def sendhtmlfilp2():
    return render_template("upfile6.html")

@app.route("/upfile6", methods=['POST'])
def flipp2():
    if request.method == 'POST':
        file = request.files['file']
        print(f"File uploaded: {file.filename}")
        # ** convert file to opencv-image **
        cimg = Image.open(file)
        crimg = np.array(cimg)
        
        output = cv2.flip(crimg, -1)  #上下左右翻轉
        flip_filename = "flip_image.png"
        cv2.imwrite(flip_filename, output)
        
    return send_file(flip_filename, mimetype="image/png")

@app.route("/up01")
def up01():
    return render_template("confile.html")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=888)
