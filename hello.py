from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
from helpers import *
import subprocess
#import MaxPlus

app     = Flask(__name__)
app.config.from_object("config")
image_rendered=False

ALLOWED_EXTENSIONS = set(['max'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html",image_rendered=image_rendered)

@app.route("/upload", methods=["POST"])
def upload_file():

	# A
    if "user_file" not in request.files:
        return "No user_file key in request.files"

	# B
    file = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

	# C.
    if file.filename == "":
        return "Please select a file"

	# D.
    if file and allowed_file(file.filename):
    	print("file.content_type:"+str(file.content_type))
    	file.filename = secure_filename(file.filename)
    	output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"])
    	flash('File Successfully uploaded to location:'+str(output))
    	return redirect("/")
    	#return str(output)

    else:
    	flash("File not uploaded",'err')
    	return redirect("/")

@app.route("/fetchModels", methods=["GET"])
def get_models():
	models = []
	objects = read_models_in_s3()
	for key in objects:
		models.append(key['Key'])
		print(key['Key'])
	flash("Successfully Fetched Models from S3_Bucket",'info')
	return render_template('index.html', models=models)

@app.route("/render", methods=["POST"])
def render_to_3dsmax():
	selected_model = request.form.get('select_model')
	width = request.form['width']
	height = request.form['height']
	pixel_offset = request.form['pixel_offset']
	print("selected_model:"+str(selected_model)+":width:"+str(width)+":height:"+str(height)+":pixel_offset:"+str(pixel_offset))
	print("Downloading 3dsMax Scene File to local")
	flash("Downloading 3dsMax Scene File to local",'info')
	download_model_from_s3(selected_model)
	#modify_pixel_offset(selected_model,pixel_offset)
	cmd_txt =  '"D:\\Program Files\\Autodesk\\3ds Max 2019\\3dsmaxcmd.exe" -outputName:"D:\\Geekie\\Computer_Graphics\\Projects\\Render Automation\\3drendererFlaskUI\\myImage.jpg" -w '+str(width)+" -h "+str(height)+' "D:\\Geekie\\Computer_Graphics\\Projects\\Render Automation\\3drendererFlaskUI\\'+str(selected_model)+'"'
	print("running cmd: "+cmd_txt)
	print("Rendering in 3dsMax")
	flash("Rendering in 3dsMax",'info')
	subprocess.call(cmd_txt, shell=True)
	print("Rendering Complete")
	flash("Rendering Complete",'info')
	print("Uploading to S3_Bucket")
	upload_image_to_s3("myImage0000.jpg")
	print("Upload Complete")
	image_rendered=True
	return render_template('index.html',image_rendered=image_rendered)

def modify_pixel_offset(scene,offset):
	fm = MaxPlus.FileManager
	fm.Open(MaxPlus.PathManager.GetTempDir() + r+str(scene))

if __name__ == "__main__":
    app.run()