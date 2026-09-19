CREATE DATABASE fb_ads_analysis;
USE fb_ads_analysis;

WITH campaign_kpis AS (
SELECT xyz_campaign_id, 
SUM(Impressions) AS impressions,
SUM(Clicks) AS clicks,
ROUND(SUM(Spent), 2) AS spent,
SUM(Total_Conversion) AS enquiry,
SUM(Approved_Conversion) AS conversions
FROM fb_ads
GROUP BY xyz_campaign_id)

SELECT xyz_campaign_id, spent, impressions, clicks, enquiry, conversions,
ROUND((100.0* clicks/NULLIF(impressions, 0)), 3) AS CTR,
ROUND((spent/NULLIF(clicks, 0)), 2) AS CPC,
ROUND((spent/NULLIF(conversions, 0)), 2) AS CPA,
ROUND((100.0* enquiry/NULLIF(clicks, 0)), 2) AS click_to_enquiry_rate,
ROUND((100.0* conversions/NULLIF(clicks, 0)), 2) AS conversion_rate,
ROUND((100.0* conversions/NULLIF(enquiry, 0)), 2) AS Enquiry_to_Sales_rate
FROM campaign_kpis
ORDER BY CPA ASC;           # sorts campaigns from lowest to highest CPA

WITH campaign_kpis AS (
SELECT xyz_campaign_id, 
SUM(Impressions) AS impressions,
SUM(Clicks) AS clicks,
ROUND(SUM(Spent), 2) AS spent,
SUM(Approved_Conversion) AS conversions
FROM fb_ads
GROUP BY xyz_campaign_id)

SELECT xyz_campaign_id, spent, 
ROUND(100.0 * spent / SUM(spent) OVER (), 2) AS spend_share_pct, conversions,
ROUND(100.0 * conversions / SUM(conversions) OVER (), 2) AS conversion_share_pct,
ROUND(spent / NULLIF(conversions, 0), 2) AS cpa
FROM campaign_kpis
ORDER BY xyz_campaign_id;

WITH segment_kpis AS (
SELECT xyz_campaign_id, age, gender,
ROUND(SUM(Spent), 2) AS spent,
SUM(Approved_Conversion) AS conversions
FROM fb_ads
GROUP BY xyz_campaign_id, age, gender
HAVING SUM(Approved_Conversion) > 0)

SELECT xyz_campaign_id, age, gender, spent, conversions,
ROUND((spent/conversions), 2) AS CPA,
RANK () OVER(PARTITION BY xyz_campaign_id ORDER BY spent/conversions ASC) AS efficiency_rank
FROM segment_kpis
ORDER BY xyz_campaign_id, efficiency_rank;

SELECT ad_id, xyz_campaign_id, age, gender, Impressions, Clicks,
ROUND((Spent), 2) AS spent, Total_Conversion, Approved_Conversion
FROM fb_ads
WHERE Approved_Conversion = 0 AND Spent > 0
ORDER BY spent DESC
LIMIT 25;

SELECT xyz_campaign_id, 
SUM(Total_Conversion) AS Enquiry,
SUM(Approved_Conversion) AS Sales,
ROUND((100.0* SUM(Approved_Conversion)/NULLIF(SUM(Total_Conversion), 0)), 2) AS Enquiry_to_Sales_rate
FROM fb_ads
GROUP BY xyz_campaign_id
ORDER BY Enquiry_to_Sales_rate DESC;