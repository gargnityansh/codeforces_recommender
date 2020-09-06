#imorting TfidfVectorizer from sklearn
#tfidf vector gives a score proportional to the value count
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd


#problem_dataframe to calculate matrix
problem_data = pd.read_csv(r'problem_sets_data.csv')

#generating matrix
tfidf = TfidfVectorizer(stop_words = 'english')
tfidf_matrix = tfidf.fit_transform(problem_data['vector'])

#generating cosine_similarity
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#indices for reverse mapping to find problem
indices = pd.Series(problem_data.index, index=problem_data['name']).drop_duplicates()

#generating recommendations
def get_recommendations(in_dataframe, name, recommended_df,from_df=problem_data, cosine_sim=cosine_sim):
	idx = indices[name]
	try:
		sim_scores = list(enumerate(cosine_sim[idx]))
		sim_scores = sorted(sim_scores, key= lambda x:x[1], reverse=True)
	except:
		pass

	sim_scores = sim_scores[1:50]
	problem_indices = [i[0] for i in sim_scores]
	for problem_id in problem_indices:
		problem_name = from_df['name'].iloc[problem_id]
		if problem_name in in_dataframe['name'].values:
			continue
		else:
			recommended_df = recommended_df.append(from_df.iloc[problem_id], ignore_index=True)
	return recommended_df
'''
recommended_df = pd.DataFrame()
in_dataframe = pd.DataFrame({'contestId':'47','index':'A' ,'name':['two'],'tags':'dp greedy', 'rating':'800', 'solvedCount':'50187','vector':'dp greedy 50187'})
k = get_recommendations(in_dataframe,'Spreadsheet',recommended_df)
print(k.head())
'''

def user_recommendation(user_dataframe, strong_dataframe):
	user_recommendations_df = pd.DataFrame()
	for index, row in user_dataframe.iterrows():
		try:
			user_recommendations_df = get_recommendations(strong_dataframe, row['name'], user_recommendations_df, problem_data,cosine_sim)
		except:
			pass

	return user_recommendations_df.drop_duplicates().sort_values('solvedCount', ascending='False')

'''in_dataframe = pd.DataFrame({'contestId':'47','index':'A' ,'name':['Distinct Digits'],'tags':'brute force implementation', 'rating':'800.0', 'solvedCount':'15860','vector':'brute force implementation 800.0'})
k = user_recommendation(in_dataframe)
print(k.head())
'''