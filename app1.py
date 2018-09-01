from flask import Flask, request
from hunspell import Hunspell

app = Flask(__name__)

@app.route("/find")
def main():
	word = request.args.get('word')
	h = Hunspell();
	sugg = h.suggest(word)
	s = "Suggestions: " + str(sugg)
	return s
if __name__ == "__main__":
	app.run(host='0.0.0.0')
