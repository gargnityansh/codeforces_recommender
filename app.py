from flask import Flask, render_template, request
import user_data_recommendation

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('base.html')

@app.route('/recommend', methods=['POST'])
def recommend():
	if not request.form.get('userhandle'):
		return "type a userhandle"
	handle = request.form.get('userhandle')
	s_data, w_data = user_data_recommendation.user_dataframe(handle)
	s,w = user_data_recommendation.problems_recommended(s_data, w_data)
	return str(s)+ ' ' + str(w)


if __name__ == '__main__':
	app.run(debug = True)