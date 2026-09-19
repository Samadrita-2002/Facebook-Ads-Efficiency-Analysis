# Facebook Ads Campaign Efficiency Analysis: Conversion, CPA & Audience Segmentation

## The business question
Three ad campaigns ran. Which one should we scale our budget into? The obvious answer is "whichever converted most" — but that's usually wrong. A campaign can win on conversion volume while being far more expensive per customer acquired. This project is about efficiency, not just effectiveness.

## Data source
Facebook Ad Campaign dataset — Kaggle (~1,143 ads, 3 campaigns)

## Important note
Users were NOT randomly assigned between campaigns — each campaign targeted
different audiences (visible in the age/gender distribution). This is a
quasi-experiment, not a controlled A/B test, so differences in performance
may partly reflect audience targeting rather than campaign quality. Segment-
level analysis (CPA by age/gender) is included to partially address this.

## Hypothesis
Null hypothesis(H0): No significant difference between campaign outcomes, i.e.,
                        conversion rate is independent of campaign
Alternative Hypothesis (H1): Significant difference between campaign outcomes, i.e.,
                       different campaigns result in different conversion rates, i.e.,
                       at least one campaign differs.
We consider level of significance (α) = 0.05
If p-value <= α — we reject the null hypothesis

## Tools
Excel (Pivot tables) → Python/pandas + scipy.stats
(data cleaning, hypothesis testing) → MySQL (further analysis) → Power BI (dashboard)

## Methodology
- Engineered standard ad KPIs: CTR, CPC, Conversion Rate, CPA, Enquiry-to-Sale rate
- Chi-square test across campaigns, with pairwise comparisons using a Bonferroni correction for multiple testing
- Segment-level CPA ranking to identify efficient audiences within each campaign

## Key findings
- With a p-value of < 0.05, we rejected the null hypothesis: Significant difference between campaign outcomes, i.e., different campaigns result in different conversion rates, i.e., at least one campaign differed.
- All three pairwise comparisons remained significant after Bonferroni correction (α = 0.0167).
- Segmentwise efficiency ranking showed that in the 916 Ad campaign, Females in the 40-44 age group were associated with the least Cost-per-Acquisition, in the 936 Campaign, it was the Males in the 30-34 age group, as was the case for the 1178 Campaign.
- Listing the top 25 ads with wasted budget (positive spent but zero acquisition), we found that 24 of them belonged to Campaign 1178, highlighting a concentration of high-spend/no-sale ads within that campaign, which is also emphasised by a significantly low conversion rate of 2.42%. Those 25 ads represent $5,569.14 in spend, of which $5,388.92 came from Campaign 1178. That is roughly 9.7% of Campaign 1178's total spend among those 24 ads alone.
- Campaigns showed relatively similar CPCs, but substantially different post-click conversion rates.
- Campaign 1178 consumed 94.82% of total advertising spend and generated 80.82% of total approved conversions. Meanwhile, Campaign 916 consumed only 0.26% of spend but generated 2.22% of conversions. However, that doesn't mean "916 is definitely the best campaign" because, as we've already noted, the campaigns were not randomly assigned and their audiences differ.
- Campaign 916 shows the highest conversion rate (21.24%) and Enquiry-to-Sales rate (41.38%) with the lowest CPA (6.24), whereas Campaign 1178 shows the lowest conversion rate (2.42%) and Enquiry-to-Sales rate (32.67%) with the highest CPA (63.83%). 
- For Campaign 916 -> 51.33% clicks turn to enquiry -> 41.38% of that enquiry become sales, whereas for Campaign 1178 -> only 7.4% clicks turn to enquiry -> 32.67% of that enquiry become sales. So, Campaign 1178 isn't necessarily struggling at the final enquiry -> sale stage alone. Its much larger weakness is earlier as a substantially smaller proportion of clicks progress to enquiries.

## Recommendations / Business Implications
- Although segment-level CPA varied substantially within campaigns, extremely low-CPA segments based on very few conversions should be treated cautiously. For example, the lowest CPA segment in Campaign 916 had only one conversion.
- In Campaign 1178, CPA ranged from $30.77 for males aged 30–34 to $137.76 for females aged 45–49, indicating that aggregate campaign performance can mask meaningful audience-level differences. So, evaluate audience segments separately when allocating or testing budget rather than relying solely on campaign-level averages.
- The similar CPCs but substantially different post-click conversion rates suggests that differences in downstream conversion performance warrant more investigation than click acquisition cost alone.
- Campaign 1178 generated the majority of conversions (80.82%) but also consumed 94.82% of total spend. Its CPC (Cost-per-click) was only modestly higher than the other campaigns, while its conversion rate was substantially lower (2.42%). This suggests that the primary performance gap may occur after users click rather than at the click-acquisition stage. 1178 deserves investigation at the funnel/segment level because its very large spend isn't translating proportionally into conversions.
- Even though Campaign 916 technically shows the highest conversion rate and Enquiry-to-Sales rate with the lowest CPA, whether its efficiency would survive scaling is the genuinely interesting analytical point: small campaigns often look efficient precisely because they're small — they're hitting the easiest-to-convert slice of an audience. Pouring budget in usually means reaching progressively less responsive people, and CPA rises. So "scale 916" isn't automatically the right recommendation; "test scaling 916 incrementally and watch whether CPA holds" is the more defensible one.
- The substantially low click-to-enquiry rate of Campaign 1178 suggests investigating the post-click experience, offer/message alignment, landing page, targeting, or lead qualification process. But since this dataset doesn't contain those variables, I can't establish these as the causes, rather as areas for further investigation.

## Limitations

- Campaigns were not randomly assigned, so observed differences cannot be interpreted as causal effects of campaign strategy alone.
- Campaigns targeted different age/gender audiences, creating potential confounding from audience composition.
- Segment-level CPA estimates based on very few conversions may be unstable.
- The analysis does not contain information about ad creative, landing pages, bidding strategy, revenue, profit or customer lifetime value.
- The "wasted budget" analysis focuses on the 25 highest-spending ads with zero approved conversions rather than all zero-conversion ads.
- Statistical significance does not by itself establish business significance or causality.

## Dashboard
[Dashboard](https://github.com/Samadrita-2002/Credit_Risk_Analysis/blob/main/dashboard.png)

## Files
- [cleaned dataset](https://github.com/Samadrita-2002/Credit_Risk_Analysis/blob/main/cleaned_credit_risk.csv)
- [Python:cleaning and feature engineering](https://github.com/Samadrita-2002/Credit_Risk_Analysis/blob/main/credit_risk_analysis.py)
- [SQL: analysis queries](https://github.com/Samadrita-2002/Credit_Risk_Analysis/blob/main/Credit_risk_queries.sql)
- [Queries outputs and pivot table](https://github.com/Samadrita-2002/Credit_Risk_Analysis/blob/main/sql_query%20results_and%20pivot%20table.xlsx)
- [Power BI file](https://github.com/Samadrita-2002/Credit_Risk_Analysis/blob/main/Credit%20Risk%20Analysis%20Dashboard.pdf)