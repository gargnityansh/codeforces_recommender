import pandas as pd
import requests
from problem_set_data import convertToString
import recommendation

def createLink(row):
	s = '<a href="https://codeforces.com/problemset/'+str(row['contestId']) +"/"+row['index']+">"+row['name']+"</a>"
	return s

#returns user submissions
def user_dataframe(handle):
	response = requests.get('https://codeforces.com/api/user.status?handle={}'.format(handle))
	response = response.json()
	if response['status']=='FAILED':
		return response['result']

	user_df = pd.DataFrame(columns=['contestId', 'index', 'name', 'rating', 'tags', 'verdict'])
	for row in response['result']:
		cont_id = row['problem']['contestId']
		prob_ind = row['problem']['index']
		prob_name = row['problem']['name']
		if 'rating' in row['problem']:
			rat = row['problem']['rating']
		else:
			rat = float("NaN")
		tag = row['problem']['tags']
		ver = row['verdict']
		dit = {'contestId':cont_id,'index': prob_ind,'name':prob_name,'rating':rat,'tags':tag,'verdict':ver}
		user_df = user_df.append(dit, ignore_index=True)
	
	user_df['tags'] = user_df['tags'].apply(convertToString)
	strong_areas = user_df[user_df['verdict']=='OK']
	weak_areas = user_df[~user_df['name'].isin(strong_areas['name'])]
	
	return strong_areas, weak_areas

#returns recommende problems as strong_areas_problem and weak_areas_problem
#as per problem verdict is ok or not
def problems_recommended(strong_areas, weak_areas):
	strong_areas_problem = recommendation.user_recommendation(strong_areas, strong_areas)
	weak_areas_problem = recommendation.user_recommendation(weak_areas, strong_areas)
	strong_areas_problem['links'] = strong_areas_problem.agg(lambda x: f"<a href=\"https://codeforces.com/problemset/problem/{x['contestId']}/{x['index']}\">{x['name']}</a>", axis=1)
	weak_areas_problem['links'] = weak_areas_problem.agg(lambda x: f"<a href=\"https://codeforces.com/problemset/problem/{x['contestId']}/{x['index']}\">{x['name']}</a>", axis=1)
	return strong_areas_problem, weak_areas_problem

'''s_data, w_data = user_dataframe('bloodytiger')
s,w = problems_recommended(s_data, w_data)
print(s.head())
print(w.head())'''