from flask import Flask, render_template, request
import user_data_recommendation
import pandas as pd

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
	return render_template('success.html',  tables=[s.to_html(classes='data', header="true", render_links=True, escape=False)],titles =s.columns.values ,wtables=[w.to_html(classes='data', header="true", render_links=True,escape=False)],wtitles =w.columns.values)


if __name__ == '__main__':
	app.run(debug = True)