import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Page config
st.set_page_config(page_title="📚 Book Genre Dashboard", layout="wide")

# Load data
df = pd.read_csv("All_Books.csv")
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
df["Rating_Num"] = df["Rating"].map(rating_map)
df["InStock"] = df["Availability"].str.contains("In stock")

# Sidebar filters
st.sidebar.header("🔍 Filter Books")
selected_genre = st.sidebar.multiselect("Select Genre(s)", df["Genre"].unique(), default=df["Genre"].unique())
min_price, max_price = st.sidebar.slider("Price Range (£)", float(df["Price"].min()), float(df["Price"].max()), (float(df["Price"].min()), float(df["Price"].max())))

filtered_df = df[(df["Genre"].isin(selected_genre)) & (df["Price"] >= min_price) & (df["Price"] <= max_price)]

# Title
st.title("📊 Exploratory Data Analysis on Book Genres")

col1, col2, col3, col4, col5 = st.columns([1,7,5,5,1])

with col4:
    # Stock status
    st.subheader("📦 Stock Status by Genre")
    stock_counts = filtered_df.groupby("Genre")["InStock"].value_counts().unstack()
    fig4, ax4 = plt.subplots()
    stock_counts.plot(kind="bar", stacked=True, ax=ax4, color=["#517FFF", "#76CDE7"])
    plt.xticks(rotation=45)
    st.pyplot(fig4)


with col2:
   # Genre distribution
    st.subheader("📌 Genre Distribution")
    genre_counts = filtered_df["Genre"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(genre_counts, labels=genre_counts.index, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

with col3:
    # Price distribution
    st.subheader("💰 Price Distribution by Genre")
    fig2, ax2 = plt.subplots()
    sns.boxplot(x="Genre", y="Price", data=filtered_df, ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# Create two columns
col1, col2 = st.columns(2)

# Left column: Top 5 cheapest books
with col1:
    st.subheader("📉 Top 5 Cheapest Books")
    cheapest = filtered_df.sort_values(by="Price").head(5)
    st.table(cheapest[["Title", "Genre", "Price"]])

# Right column: Top 5 most expensive books
with col2:
    st.subheader("📈 Top 5 Most Expensive Books")
    expensive = filtered_df.sort_values(by="Price", ascending=False).head(5)
    st.table(expensive[["Title", "Genre", "Price"]])


col1, col2 = st.columns(2)

with col1:
    # Price vs Rating
    st.subheader("📈 Price vs Rating")
    fig5, ax5 = plt.subplots()
    sns.scatterplot(x="Rating_Num", y="Price", hue="Genre", data=filtered_df, ax=ax5)
    st.pyplot(fig5)


 
with col2:
    # Average price per rating
    st.subheader("💵 Average Price by Rating")
    avg_price_rating = filtered_df.groupby("Rating_Num")["Price"].mean().reset_index()

    fig6, ax6 = plt.subplots()
    sns.barplot(x="Rating_Num", y="Price", data=avg_price_rating, ax=ax6, color="#E2AFE2")
    ax6.set_ylabel("Average Price (£)")
    st.pyplot(fig6)

col1, col2, col3 = st.columns([1,3,1])
with col2:
   # Rating breakdown (percentage per genre)
    st.subheader("⭐ Rating Distribution (Percentage per Genre)")

    #    Calculate percentage
    rating_counts = filtered_df.groupby(["Genre", "Rating_Num"]).size().reset_index(name="Count")
    genre_totals = filtered_df["Genre"].value_counts().to_dict()
    rating_counts["Percentage"] = rating_counts.apply(lambda row: row["Count"] / genre_totals[row["Genre"]] * 100, axis=1)

    pink_palette = [
        "#000000", "#2C2C2C", "#4B3F4E", "#6E4C6E", "#8B5C7E", "#A86C8C", "#C48C9E", "#E1A6B4"
    ]
    
    # Create histogram-style grouped bar chart
    fig3 = px.histogram(
        rating_counts,
        x="Rating_Num",
        y="Percentage",
        color="Genre",
        barmode="group",
        hover_data=["Genre", "Rating_Num", "Percentage"],
        labels={"Rating_Num": "Rating", "Percentage": "Percentage (%)"},
        color_discrete_sequence=pink_palette
    )

    fig3.update_layout(
        yaxis_title="Percentage (%)",
        xaxis_title="Rating",
        legend_title="Genre",
        bargap=0.15
    )
    
    st.plotly_chart(fig3, use_container_width=True)


# Data preview
st.subheader("📄 Filtered Book List")
st.dataframe(filtered_df[["Title", "Genre", "Price", "Rating", "Availability"]])

#Listed stock out books
st.subheader("❗ Stock Out Books")
stock_out_books = filtered_df[filtered_df["Availability"] == "Stock out"]
st.dataframe(stock_out_books[["Title", "Genre", "Price", "Rating", "Availability"]])
st.write(f"Total Stock Out Books: {len(stock_out_books)}")
st.write(f"Percentage of Stock Out Books: {len(stock_out_books) / len(filtered_df) * 100:.2f}%")

# Footer
st.markdown("___")
col_left, col_right = st.columns([3, 1])
with col_right:
    st.markdown("Developed by [Mayesha Afrooz](https://www.linkedin.com/in/mayeshaafrooz/)")

    st.markdown("Data Source: [Books to Scrape](http://books.toscrape.com/)")



