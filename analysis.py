import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# cleaned dataframe earlier using google colab code, and then i just downloaded the files so im not doing any cleaning here
df1 = pd.read_csv('df1.csv')  
df2 = pd.read_csv('df2.csv')
df3 = pd.read_csv('df3.csv')

# interested in finding the age of all the participants and seeing if any answers correlate specifically with age (not graduate students because grad students are older)
temp1 = df1[["How old are you?"]]
temp2 = df2[["How old are you?"]]
temp3 = df3[["How old are you?"]]

# concatenate the DataFrames vertically
combined = pd.concat([temp1, temp2, temp3], ignore_index = True)

# define bins for ages 19, 20, 21, and 22+
bins = [17, 19, 20, 21, np.inf]
labels = ['19 and under', '20', '21', '22+']

# create a new column for binned ages
combined['age_group'] = pd.cut(combined['How old are you?'], bins = bins, labels = labels, right = False)

# create a histogram of the binned ages, this is just to help visualize the distribution and i was curious about it
plt.figure(figsize = (10, 6))
sns.histplot(combined['age_group'], bins = len(labels))
plt.title('Histogram of Ages')
plt.xlabel('Age Group')
plt.ylabel('Frequency')


df1['age_group'] = pd.cut(df1["How old are you?"], bins = bins, labels = labels, right = False)
df2['age_group'] = pd.cut(df2["How old are you?"], bins = bins, labels = labels, right = False)
df3['age_group'] = pd.cut(df3["How old are you?"], bins = bins, labels = labels, right = False)

dfs = [df1, df2, df3]

print('\n ------------------- AGE VS. QUESTION -------------------\n')

count = 1
for df in dfs:
    colStart = 7
    name = ''

    # identifying the dataframe
    if count == 1:
        name = 'Max 2024'
    elif count == 2:
        name = 'Fardina 2023'
        colStart = 8
    else:
        name = 'Max 2023'

    question_cols = df.columns[colStart:-1]

    for question_col in question_cols:
        contingency_table = pd.crosstab(df['age_group'], df[question_col])
        chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

        if p < 0.05:
            print("Dataframe: ", name)  # printing dataframe
            print(f"Question: {question_col[:40]}...")
            print(f"P-value: {p}")
            print("-" * 20) 

            # create a heatmap of the contingency table
            plt.figure(figsize = (12, 8))
            sns.heatmap(contingency_table, annot = True, fmt = "d", cmap = "YlGnBu")
            plt.title(f'Heatmap of Age vs Jerk Rating of: {question_col[:40]}...')
            plt.xlabel('Jerk Rating')
            plt.ylabel('Age Group')
            plt.show(block = False)
            plt.pause(1)  # pause for map rendering
    
    count += 1

    # i just wanted to see if any of the answers correlated with age, so i used chi-squared test to see if the p-value was less than .05
    # but none of the p values were greater than .05 so i didnt find any correlation between age and the answers

# something else i was curious about was whether gender was correlated with any of the answers
# so i did the same thing as above but with gender instead of age
# this time I don't need to create bins, but I can just run chi squared tests on each dataframe
print('\n ------------------- GENDER VS. QUESTION -------------------\n') 


temp1 = df1['What bests represents your gender?']
temp2 = df2['What bests represents your gender?']
temp3 = df3['What bests represents your gender?']

# concatenate the dfs vertically
combined = pd.concat([temp1, temp2, temp3], ignore_index = True)

# first create a histogram of the gender distributions for my own curiosity
plt.figure(figsize = (10, 6))
sns.histplot(combined, discrete = True)
plt.title('Histogram of Gender Distribution')
plt.xlabel('Gender')
plt.ylabel('Frequency')

count = 1

# same thing as above
for df in dfs:
    colStart = 7
    name = ''

    if count == 1:
        name = 'Max 2024'
    elif count == 2:
        name = 'Fardina 2023'
        colStart = 8
    else:
        name = 'Max 2023'

    question_cols = df.columns[colStart:-1]

    for question_col in question_cols:
        contingency_table = pd.crosstab(df['What bests represents your gender?'], df[question_col])
        chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
        
        # also print heatmap of the contingency table if it's significant
        if p < 0.05:
            print("Dataframe: ", name)  
            print(f"Question: {question_col[:40]}...")
            print(f"P-value: {p}")
            print("-" * 20)    

            # heatmap of the contingency table
            plt.figure(figsize = (12, 8))
            sns.heatmap(contingency_table, annot = True, fmt = "d", cmap = "YlGnBu")
            plt.title(f'Heatmap of Gender vs Jerk Rating of: {question_col[:40]}...')
            plt.xlabel('Jerk Rating')
            plt.ylabel('Gender')
            plt.show(block = False)
            plt.pause(1)  

            # create paired bar chart with gender on the x-axis
            melted_df = df.melt(id_vars = ['What bests represents your gender?'], value_vars = [question_col], var_name = 'Question', value_name = 'Jerk Rating')
            sns.catplot(data = melted_df, x = 'What bests represents your gender?', hue = 'Jerk Rating', kind = 'count', height = 6, aspect = 1.5, palette = 'viridis')
            plt.title(f'Paired Bar Chart of Gender vs Jerk Rating of: {question_col[:40]}...')
            plt.xlabel('Gender')
            plt.ylabel('Frequency')
            plt.xticks(rotation = 0)  
            plt.tight_layout()
            plt.show(block = False)
            plt.pause(1)  
    
    count += 1

plt.show()  # show all plots at the end
