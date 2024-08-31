from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
from werkzeug.middleware.proxy_fix import ProxyFix
import os

app = Flask(__name__)

# Apply ProxyFix to handle forwarded headers if behind a reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=0)

# Global variable to store the camera source and capture object
camera_source = 0
cap = None

def generate_frames():
    global cap
    if not cap or not cap.isOpened():
        print("Error: Could not open camera.")
        return b''

    while True:
        success, frame = cap.read()
        if not success:
            print("Error: Failed to read frame.")
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Failed to encode frame.")
                continue
            frame = buffer.tobytes()

            # Yield the frame as a byte array
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/', methods=['GET', 'POST'])
def index():
    global camera_source, cap
    if request.method == 'POST':
        # Get the camera input from the form
        camera_input = request.form.get('camera_input')

        # Check if input is a digit (camera index) or URL (IP camera)
        if camera_input.isdigit():
            camera_source = int(camera_input)
        else:
            camera_source = camera_input

        # Release the current camera and reinitialize with the new source
        if cap:
            cap.release()

        cap = cv2.VideoCapture(camera_source)

        if not cap.isOpened():
            print(f"Error: Could not open camera with source: {camera_source}")

        return redirect(url_for('index'))

    # Renders the index.html file
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Returns the response generated along with the specific media type (mime type)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # Run with self-signed certificates (for development purposes)
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
