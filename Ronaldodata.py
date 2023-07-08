import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import sys
import matplotlib
import matplotlib.patches as patch
import seaborn as sns

df_cris = pd.read_csv("data.csv")
df_cris['Goal_assist'].fillna("Not assisted", inplace=True)
df_cris['Type'].fillna("Regular goal", inplace=True)
df_cris['Playing_Position'].fillna("Unknown", inplace=True)
df_cris['Date'] = df_cris['Date'].astype('datetime64[ns]')

home_goals = df_cris['Venue'].value_counts()['H'] # total no of home goals scored
print("The total number of Home Goals CR7 has scored is:", home_goals)
# df_cris = df_cris.loc[df_cris['Venue']=='H']  #displays only the stats of home games
df_cris.index = np.arange(1, len(df_cris) + 1) #index starts from 1 instead of 0
# df_cris.to_csv('all_home_goals.csv') #-- creates a csv with all home goals scored by cris
sorted_df = df_cris['Opponent'].value_counts().head() #displays the top 5 opponents hes score more against
df_cris.rename(columns = {'count':'Goals'})
matplotlib.style.use('fivethirtyeight')
sns.set_style("dark")
sorted_df.plot.bar(x = 'Opponent', y = 'count',stacked = True, color = '#42f5b0')
plt.title("Ronaldo's favourite opponents", fontsize =20)
plt.xlabel("Opponent", fontsize = 15)
plt.ylabel("Goals", fontsize = 15)
# plt.show()
# sorted_df.to_csv('favourite opponent.csv')
# df_cris = df_cris.replace('90+5', 95)
df_cris = df_cris.replace('90+5', 95)
df_cris = df_cris.replace('90+1', 91)
df_cris = df_cris.replace('90+7', 97)
df_cris = df_cris.replace('90+6', 96)
df_cris = df_cris.replace('90+4', 94)
df_cris = df_cris.replace('90+3', 93)
df_cris = df_cris.replace('90+2', 92)
df_cris = df_cris.replace('45+1', 45)
df_cris = df_cris.replace('45+2', 45)
df_cris = df_cris.replace('45+3', 45)
df_cris = df_cris.replace('45+4', 45)
df_cris = df_cris.replace('45+5', 45)
df_cris = df_cris.replace('45+6', 45)
df_cris = df_cris.replace('45+7', 45)
df_cris['Minute'] = pd.to_numeric(df_cris['Minute'])
# print(df_cris['Minute'].dtypes)
fav_minute = df_cris['Minute']
fav_minute = df_cris.sort_values(by = ['Minute'], ascending=False)
#to retrieve goals score from 91st min to 120th min
goals_btw_91_120 = fav_minute['Minute'].head(28)
goals_btw_91_120.index = np.arange(1, len(goals_btw_91_120) + 1)
total_91_120 = goals_btw_91_120.value_counts().sum()
#to retrieve goals scored from 61st min to 90th min
goals_btw_61_90 = fav_minute[(fav_minute['Minute']>=61) & (fav_minute['Minute']<=90)]
goals_btw_61_90.index = np.arange(1, len(goals_btw_61_90) + 1)
total_61_90 = goals_btw_61_90['Minute'].value_counts().sum()
#to retrieve goals scored from 31st min to 60th min
goals_btw_31_60 = fav_minute[(fav_minute['Minute']>=31) & (fav_minute['Minute']<=60)]
goals_btw_31_60.index = np.arange(1, len(goals_btw_31_60) + 1)
total_31_60 = goals_btw_31_60['Minute'].value_counts().sum()
#to retrieve goals scored from 1st min to 30th min
goals_btw_1_30 = fav_minute[(fav_minute['Minute']>=1) & (fav_minute['Minute']<=30)]
goals_btw_1_30.index = np.arange(1, len(goals_btw_1_30) + 1)
total_1_30 = goals_btw_1_30['Minute'].value_counts().sum()


#now creating a dataframe to use it for plotting
min_goal = [['91-120', total_91_120], ['61-90', total_61_90], ['31-60',total_31_60], ['1-30', total_1_30]]
df_min_goal = pd.DataFrame(min_goal, columns=['Minute', 'Goals'])
# print(df_min_goal)

#this code is to create line chart
matplotlib.style.use('fivethirtyeight')
# sns.set_style("dark")
df_min_goal.plot(x = 'Minute', y = 'Goals')
plt.title('Minutes at which Ronaldo usually scores goals', fontsize=20)
plt.ylabel("Goals", fontsize = 15)
plt.xlabel("Minutes", fontsize = 15)
# plt.show()
# print(df_cris)
# df_cris.to_csv('Ronaldo data cleaned.csv')
# df_cris = df_cris[df_cris.Goal_assist != 'Not assisted']
# df_cris = df_cris[df_cris.Goal_assist != '\t']
df_cris.index = np.arange(1, len(df_cris) + 1)
players_who_assisted = df_cris['Goal_assist'].value_counts()
# players_who_assisted.to_csv('players who assisted cr7.csv')
top_15 = players_who_assisted.head(10)
# print(top_15)
matplotlib.style.use('fivethirtyeight') 
sns.set_style("dark")
top_15.plot.barh(title = 'Top 10 Players who assisted Ronaldo the most', x = 'Goal_assist', y = 'Goals', stacked = True, color = ['orange'])
plt.ylabel("Goal assists")
plt.xlabel("Goals")
# plt.show()
df_cris = df_cris.drop('Matchday', axis=1)
# df_cris.to_csv('Ronaldo data cleaned.csv')



#this part of the code removes games which moved to extra time and penalty shootouts
clear_pens= df_cris[~df_cris['Result'].str.contains('pens')]
et_clear = clear_pens[~clear_pens['Result'].str.contains('AET')]
len_of_table = len(et_clear['Result'])
# print(len_of_table)
# print(df_cris.info())

ft_optimize= et_clear['Result'].str.split(':')
f_index = ft_optimize.str[0].astype(int)
l_index = ft_optimize.str[1].astype(int)
formatted_values_ft = f_index.astype(str) + ':' + l_index.map("{:0>1d}".format)
et_clear['Result'] = formatted_values_ft

at_optimize = et_clear['At_score'].str.split(':')
f_index_at = at_optimize.str[0].astype(int)
l_index_at = at_optimize.str[1].astype(int)
formatted_values = f_index_at.astype(str) + ':' + l_index_at.map("{:0>1d}".format)
et_clear['At_score'] = formatted_values

#to get a better result of the winning goal score we are separating the Home and away games
home_games = et_clear[et_clear['Venue'].str.contains('H')]
away_games = et_clear[et_clear['Venue'].str.contains('A')]

#this code stores the goals which he was last to score
home_g= []
for index, row in home_games.iterrows():
    if row['Result'] == row['At_score']:
        home_g.append(row)
        
home_lg = pd.DataFrame(home_g)
# print(home_lg['At_score'])
# home_lg.to_csv('home_l_g.csv')

away_g= []
for index, row in away_games.iterrows():
    if row['Result'] == row['At_score']:
        away_g.append(row)
        
away_lg = pd.DataFrame(away_g)
# print(away_lg['At_score'])
# away_lg.to_csv('away_lg.csv')

#to calculate ho many winner or equalizers playing home
h1_index = home_lg['Result'].str.split(':').str[0]
h2_index = home_lg['Result'].str.split(':').str[1]
home_lg['W_or_L'] = ['W' if int(f) > int(l) else ('T' if int(f) == int(l) else 'L') for f, l in zip(h1_index, h2_index)]
# print(home_lg)
# home_lg.to_csv('home_l_g.csv')

a1_index = away_lg['Result'].str.split(':').str[0]
a2_index = away_lg['Result'].str.split(':').str[1]
away_lg['W_or_L'] = ['W' if int(f) < int(l) else ('T' if int(f) == int(l) else 'L') for f, l in zip(a1_index, a2_index)]
# print(away_lg)
# away_lg.to_csv('away_lg.csv')

#contains lg of both H and A
new_df = pd.concat([home_lg, away_lg], ignore_index=True)
# new_df.to_csv('H_A_Winner.csv')
wins = new_df[new_df['W_or_L'] == 'W']
print(wins['W_or_L'].value_counts())
winner_89to90plus = wins[wins['Minute']>=90]
winner_89to90plus = winner_89to90plus[['Minute', 'Club']].value_counts()
winner_89to90plus.to_csv('Winning goals scored after 90 mins.csv')
print(winner_89to90plus)
grouped_df = winner_89to90plus.groupby(['Minute', 'Club']).sum().reset_index()

# # Plot the bar graph
# fig, ax = plt.subplots(figsize=(10, 6))
# colors = plt.cm.get_cmap('tab20c', len(grouped_df['Club'].unique()))

# for i, club in enumerate(grouped_df['Club'].unique()):
#     club_data = grouped_df[grouped_df['Club'] == club]
#     ax.bar(club_data['Minute'], club_data['count'], color=colors(i))

# # Set labels and title
# ax.set_xlabel('Minute')
# ax.set_ylabel('Goals')
# ax.set_title('Goals by Minute for Different Clubs')

# # Set legend
# legend_labels = grouped_df['Club'].unique()
# ax.legend(legend_labels, loc='upper right')

# # Display the graph
# plt.show()

# Get unique clubs
clubs = grouped_df['Club'].unique()

# Set up the figure and axis
fig, ax = plt.subplots()

# Loop through each club and plot the goals
for club in clubs:
    club_data = grouped_df[grouped_df['Club'] == club]
    ax.scatter(club_data['Minute'], club_data['count'], label=club)

# Set labels and title
ax.set_xlabel('Minute')
ax.set_ylabel('Goals')
ax.set_title('Last minute winners differentiated by clubs')

# Set legend
ax.legend()

# Display the graph
plt.show()