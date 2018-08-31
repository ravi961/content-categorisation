from flask import render_template, request
from flask import Flask
app = Flask(__name__)

@app.route('/')
<<<<<<< Updated upstream
def index():
	return render_template('index.html')
=======
	def index():
	    return render_template('index.html')

@app.route('/uploadText')
	def upload_letter():
    	if request.method == 'POST':
        	textValue = request.form['textQuery'].lstrip().rstrip()
        	return render_template()
>>>>>>> Stashed changes

if __name__ == '__main__':
	app.run(debug=True)