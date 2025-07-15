# Mobile-Game-User-Behavior-and-Revenue-Analysis-Dashboard
Analyzing the performance of a fictional mobile game based on user behavior, revenue metrics, and A/B test results; preparing decision support dashboards; making data-based recommendations.


## Project Overview

This project simulates mobile game user data, performs ETL pipelines to load data into PostgreSQL, calculates key user behavior metrics, and analyzes A/B test results. The final goal is to create interactive dashboards in Tableau for visualization.

## Project Steps

1. **Data Simulation & ETL Pipeline**  
   Generate synthetic user event data including sessions, purchases, and ad clicks with Python.  
   Load the data into PostgreSQL with automated ETL scripts.

2. **User Behavior Analysis**  
   Calculate important KPIs like DAU, retention, churn, ARPU, and LTV.  
   Conduct segment-level analyses (e.g., whales vs. casual players).

3. **Dashboard Design**  
   Create interactive Tableau dashboards visualizing user metrics and A/B test results.

4. **A/B Testing Simulation & Analysis**  
   Simulate test and control groups for new game features and statistically evaluate results.



## How to Run

1. Set up PostgreSQL and configure connection settings.  
2. Run the data simulation script:  
   `python scripts/generate_simulation_data.py`  
3. Run ETL pipeline to load data into the database:  
   `python scripts/etl_pipeline.py`  
4. Perform A/B test analysis:  
   `python scripts/ab_test_analysis.py`  
5. Connect Tableau to CSV files or PostgreSQL for dashboard visualization.

## Tableau Dashboards

Interactive dashboards for key metrics and A/B test results are published on Tableau Public:  
[https://public.tableau.com/views/Graphs_17525986128080/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link]

## Technologies Used

- Python (pandas, numpy, scipy)  
- PostgreSQL  
- Tableau (for visualization)

---

For questions or collaboration, feel free to reach out.



