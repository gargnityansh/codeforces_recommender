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
	user_recommendations_df.drop_duplicates(subset='name',inplace=True)
	user_recommendations_df.fillna(0, inplace=True)
	user_recommendations_df[['contestId', 'rating', 'solvedCount']] = user_recommendations_df[['contestId', 'rating', 'solvedCount']].astype('int64')
	user_recommendations_df.sort_values('solvedCount', ascending=False, inplace=True)
	user_recommendations_df.drop(['vector'],axis=1,inplace=True)

	return user_recommendations_df

'''
in_dataframe = pd.DataFrame({'contestId':'47','index':'A' ,'name':['Distinct Digits'],'tags':'brute force implementation', 'rating':'800', 'solvedCount':'15860','vector':'brute force implementation 800'})
k = user_recommendation(in_dataframe, in_dataframe)
k.fillna(0, inplace=True)
k[['contestId', 'rating', 'solvedCount']] = k[['contestId', 'rating', 'solvedCount']].astype('int64')
k.sort_values('solvedCount', ascending=False, inplace=True)
print(k.head())
'''