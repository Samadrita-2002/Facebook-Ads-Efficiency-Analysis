import pandas as pd
import numpy as np

df = pd.read_csv("KAG_conversion_data.csv")
print(df.head(10))
print(df.isnull().sum())

# As we already saw in Excel, there are no blank cells in this dataset

# To avoid divide-by-zero crashes, we use the nullif style guard, i.e., replace '0'
# with NaN for ads that got no clicks and impressions.

df['CTR'] = 100* df['Clicks']/df['Impressions'].replace(0, np.nan)
df['CPC'] = df['Spent']/df['Clicks'].replace(0, np.nan)          #CPC = cost per click
df['Conversion_rate'] = 100* df['Approved_Conversion']/df['Clicks'].replace(0, np.nan)        
df['CPA'] = df['Spent']/df['Approved_Conversion'].replace(0, np.nan)                  #CPA = cost per acquisition, this is the key metric
df['Enquiry_to_Sale_rate'] = 100* df['Approved_Conversion']/df['Total_Conversion'].replace(0, np.nan)

print(df.head(10))

df.to_csv("cleaned_fb_ads.csv", index=False)

print(df.groupby('xyz_campaign_id')[['CTR', 'CPC', 'Conversion_rate', 'CPA', 'Enquiry_to_Sale_rate']].mean().round(2))

#                   CTR     CPC  Conversion_rate      CPA  Enquiry_to_Sale_rate
# xyz_campaign_id                                                              
# 916              0.02  133.03            25.71   314.17                 41.67
# 936              0.02  136.42            21.21   549.62                 34.74
# 1178             0.02  157.25             5.21  5840.75                 32.62

# Now our overall question is:
# "Do the three campaigns have significantly different conversion behaviour, 
# or could the observed differences just be due to random variation?"
# To answer that we perform chi2 test of independence

from scipy.stats import chi2_contingency
# We use Chi-square statistic because we are testing the independence between categorical variables

# Null Hypotheis (H0): No significant difference between campaign outcomes, i.e.,
#                        conversion rate is independent of campaign
# Alternative Hypothesis (H1): Significant difference between campaign outcomes, i.e.,
#                        different campaigns result in different conversion rates, i.e.,
#                        at least one campaign differs.
# We consider level of significance (α) = 0.05
# If p-value <= α — we reject the null hypothesis

# Now we create the required contingency table step-by-step

campaign_summary = df.groupby('xyz_campaign_id').agg(
    total_clicks= ('Clicks', 'sum'),
    total_spent = ('Spent', 'sum'),
    total_converted = ('Approved_Conversion', 'sum')
).reset_index()

# Now we add the non-conversions to this

campaign_summary['non_converted'] = campaign_summary['total_clicks']-campaign_summary['total_converted']
print(campaign_summary)

#    xyz_campaign_id  total_clicks   total_spent  total_converted  non_converted
# 0              916           113    149.710001               24             89
# 1              936          1984   2893.369999              183           1801
# 2             1178         36068  55662.149959              872          35196

campaign_summary['conversion_rate'] = (100* campaign_summary['total_converted']/campaign_summary['total_clicks']).round(2)
campaign_summary['CPA'] = (campaign_summary['total_spent']/campaign_summary['total_converted']).round(2)
print(campaign_summary)

contingency = campaign_summary[['total_converted', 'non_converted']].values
print(contingency)

## This is the observed value table
#    xyz_campaign_id  total_converted  non_converted
# 0              916               24             89
# 1              936              183           1801
# 2             1178              872          35196

chi2, p_value, dof, expected = chi2_contingency(contingency)

expected_df = pd.DataFrame(expected.round(2),
                           columns = ['Expected_converted', 'Expected_non_converted'],
                           index = campaign_summary['xyz_campaign_id'])
print(expected_df)
## This is the expected value table
#                  Expected_converted  Expected_non_converted
# xyz_campaign_id                                            
# 916                            3.19                  109.81
# 936                           56.09                 1927.91
# 1178                        1019.71                35048.29

# Chi2 test of independence answers whether the difference between
# the observed values and the expected values are too large to 
# be attributed to random chance


print(f"Chi-square_statistic: {chi2:.2f}")        #because we want only up to two decimal points
print(f"P value: {p_value:.6f}")                  ##we're keeping p-value upto 6 decimal points so as not to hide any useful info
# Chi-square_statistic: 456.94
# P value: 0.000000

# Therefore, clearly, p_value is less than the level of significance, i.e., 0.05

if p_value <= 0.05:
    print("Significant difference between campaigns")
else:
    print("No significant difference")

# Significant difference between campaigns
# Null Hypothesis is rejected

# However, This chi-square test answered:
# "Is there any statistically significant difference among the campaigns overall?"
# And since we found a significant result, the natural next question is:
# "Which campaign pairs are actually different?"

# This is what we do now

from itertools import combinations          #This creates unique pairs (combinations of 2) of the campaigns for us to compare

campaigns = campaign_summary['xyz_campaign_id'].tolist()        #This converts the pandas series into a normal python list

len(list(combinations(campaigns, 2)))           #We get 3 from here

# If we use α = 0.05 as the level of significance again for all three pairs of campaigns,
# that increases the probability of getting at least one false positive more than 5%
# So, to tackle that issue, we create a alpha_corrected. 
# This procedure is called Bonferroni correction.

alpha_corrected = 0.05/3
print(f"Bonferroni_alpha_corrected: {alpha_corrected:.4f}")

# Bonferroni_alpha_corrected: 0.0167
# So, now for the pairwise tests, null hypothesis will be rejected if 
# p_value <= 0.0167

for a, b in combinations(campaigns, 2):
    subset = campaign_summary[campaign_summary['xyz_campaign_id'].isin([a, b])]
    chi2_p, p_value_p, dof_p, expected_p = chi2_contingency(subset[['total_converted', 'non_converted']].values)           # here _p stands for pairwise
    verdict = "Statistically Significant" if p_value_p <= alpha_corrected else "Not Significant"
    print(f"Campaigns {a} and {b}: p_value={p_value_p:.6f} -> {verdict}")

# Campaigns 916 and 936: p_value=0.000063 -> Statistically Significant
# Campaigns 916 and 1178: p_value=0.000000 -> Statistically Significant
# Campaigns 936 and 1178: p_value=0.000000 -> Statistically Significant

# Therefore, campaign 916 had the highest observed conversion rate, 
# followed by 936 and 1178, and the pairwise chi-square tests indicate that 
# the conversion-rate differences between each pair are statistically significant.

from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:password@localhost/fb_ads_analysis')
df.to_sql('fb_ads', engine, if_exists='replace', index=False)
