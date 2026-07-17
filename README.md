# 📈 Bitcoin Market Sentiment vs Trader Performance Analysis

## 📌 Project Overview

This project analyzes the relationship between **Bitcoin Market Sentiment (Fear & Greed Index)** and **historical trading performance** from Hyperliquid traders.

The objective is to explore how market sentiment influences trader behavior, profitability, leverage, and trading decisions. The project involves data cleaning, exploratory data analysis (EDA), feature engineering, and business insights to support data-driven trading strategies.

---

## 🎯 Objectives

- Analyze Bitcoin Fear & Greed sentiment over time.
- Study trader performance under different market sentiments.
- Identify profitable trading patterns.
- Explore the impact of leverage on profit and loss.
- Discover hidden trends using data visualization.
- Generate actionable business insights.

---

## 📂 Dataset

This project uses two datasets:

### 1. Bitcoin Fear & Greed Index

Contains daily market sentiment.

Columns include:

- Date
- Classification (Fear / Greed)

### 2. Historical Trader Data (Hyperliquid)

Contains historical trading records.

Columns include:

- Account
- Symbol
- Execution Price
- Size
- Side (Buy/Sell)
- Time
- Start Position
- Event
- Closed PnL
- Leverage
- etc.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

---

## 📁 Project Structure

```

```

---

## 📊 Project Workflow

### 1. Data Collection

- Load Historical Trading Dataset
- Load Bitcoin Fear & Greed Dataset

### 2. Data Preprocessing

- Handle missing values
- Remove duplicates
- Convert timestamps
- Merge datasets on Date

### 3. Exploratory Data Analysis (EDA)

Performed analysis on:

- Profit/Loss Distribution
- Fear vs Greed Distribution
- Average Profit by Market Sentiment
- Buy vs Sell Analysis
- Symbol-wise Profitability
- Trader Performance
- Leverage Analysis
- Trade Size Analysis
- Correlation Analysis

### 4. Feature Engineering

Created additional features such as:

- Trading Hour
- Trading Day
- Profit/Loss Category
- Market Sentiment Label

### 5. Business Insights

Generated insights on:

- Most profitable market sentiment
- Best-performing trading symbols
- Trader profitability
- Leverage behavior
- Market trends

---

## 📈 Visualizations

The project includes multiple visualizations such as:

- Histogram
- Count Plot
- Bar Chart
- Scatter Plot
- Box Plot
- Heatmap
- Pie Chart
- Line Chart
- Correlation Matrix

---

## 📌 Key Insights

- Compared trader profitability during Fear and Greed markets.
- Analyzed the relationship between leverage and profit.
- Identified top-performing traders and trading symbols.
- Explored the influence of market sentiment on trading behavior.

---

## 🚀 How to Run

Clone the repository

```bash
git clone https://github.com/yourusername/Bitcoin_Sentiment_Analysis.git
```

Move into the project folder

```bash
cd Bitcoin_Sentiment_Analysis
```

Install dependencies

```bash
pip install -r requirements.txt
```

Launch Jupyter Notebook

```bash
jupyter notebook
```

Open

```
analysis.ipynb
```

Run all cells.

---

## 📷 Sample Output

The notebook includes:

- Cleaned Dataset
- Statistical Summary
- Interactive Visualizations
- Business Insights
- Final Conclusions <img width="215" height="239" alt="image" src="https://github.com/user-attachments/assets/96e50644-5fda-4de8-aaed-9cb1fcfd9478" />
<img width="196" height="158" alt="image" src="https://github.com/user-attachments/assets/95b6d5f5-d8b7-4d39-b8c8-5ef0e045aaec" />



---

## 📌 Future Improvements

- Machine Learning models for profit prediction
- Time-series forecasting
- Interactive dashboard using Streamlit
- Power BI Dashboard
- Automated reporting

---

## 👩‍💻 Author

**Samyuktha**

B.Tech – Artificial Intelligence and Data Science

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile

---

## ⭐ Acknowledgements

This project was completed as part of the Data Science Hiring Assignment to analyze the relationship between Bitcoin market sentiment and trader performance using real-world trading data.
