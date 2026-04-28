Here is a clean and professional **README.md** without emojis:

---

# North American Box Office Analytics

## Overview

This project presents a data-driven analysis of North American box office performance using machine learning and visualization techniques. It integrates multi-year movie data (2005–2025) into a unified dataset to identify key factors influencing revenue and to build predictive models for domestic lifetime gross.

## Features

* Integration of multi-year datasets into a single master dataset
* Data cleaning, preprocessing, and type handling
* Feature engineering, including the legs ratio (lifetime gross / opening gross)
* Exploratory Data Analysis with multiple visualizations
* Correlation analysis between financial and release attributes
* Linear Regression model for predicting domestic lifetime gross (R² ≈ 0.73)

## Visualizations

* Opening Gross vs Domestic Lifetime Gross
* Budget vs Revenue
* MPAA Rating comparisons
* Monthly and yearly revenue trends
* Correlation heatmap of key features

## Tech Stack

* Python
* Pandas, NumPy
* Matplotlib, Seaborn
* Scikit-learn

## Project Structure

```
north-american-box-office/
│── data/                # Raw and cleaned datasets
│── notebooks/           # Analysis and visualization scripts
│── src/                 # Core processing and modeling logic
│── visualizations/      # Generated plots and outputs
│── README.md
```

## Future Work

* Implementation of advanced machine learning models
* Integration of external features such as audience sentiment
* Deployment as a web-based analytics dashboard using Flask and React

## Author

Chaitanya Kousik BSR
Computer Science and Engineering
KL University, Hyderabad, India
