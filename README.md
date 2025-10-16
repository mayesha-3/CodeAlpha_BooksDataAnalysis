# 📚 Book Genre Data Analysis

🔗 **Live App**: [books-data-analysis.streamlit.app](https://books-data-analysis.streamlit.app/)

This project explores book data scraped from [Books to Scrape](http://books.toscrape.com/) and visualizes genre-based trends using Python and Streamlit. It combines web scraping, data cleaning, and exploratory data analysis (EDA) to uncover insights across Romance, Mystery, Thriller, Classics, and Science Fiction categories.


---

## 🔍 Features
- Genre distribution (pie chart)
- Price distribution by genre (boxplot)
- Rating breakdown (percentage per genre)
- Stock status visualization (stacked bar)
- Price vs rating scatter plot
- Top 5 cheapest and most expensive books
- Filtered book list and stock-out summary
- Sidebar filters for genre and price range

---

## 🛠️ Tech Stack
- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit

---

## 🚀 Deployment
Hosted on [Streamlit Cloud](https://streamlit.io/cloud). To run locally:
```bash
pip install streamlit pandas matplotlib seaborn
streamlit run task3.py
