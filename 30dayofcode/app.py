from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Sample dataset
data = {
    "CustomerID": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    "Age": [25, 34, 22, 29, 40, 35, 28, 31, 23, 37],
    "Gender": ["M", "F", "M", "F", "M", "F", "M", "F", "M", "F"],
    "PurchaseAmount": [200, 450, 300, 150, 500, 100, 250, 400, 120, 330],
    "Category": ["Electronics", "Clothing", "Electronics", "Grocery", "Clothing", 
                 "Grocery", "Electronics", "Clothing", "Grocery", "Electronics"]
}

# Load dataset into DataFrame
df = pd.DataFrame(data)

# 1. Total purchases per category
category_totals = df.groupby("Category")["PurchaseAmount"].sum()

# 2. Average purchase per gender
avg_purchase_gender = df.groupby("Gender")["PurchaseAmount"].mean()

# 3. Average purchase per age group
df["AgeGroup"] = pd.cut(df["Age"], bins=[20, 30, 40, 50], labels=["20-30", "30-40", "40-50"])
age_group_avg = df.groupby("AgeGroup")["PurchaseAmount"].mean()

# Function to save visualizations
def save_plot():
    plt.figure(figsize=(12, 5))

    # Barplot for purchases per category
    plt.subplot(1, 3, 1)
    sns.barplot(x=category_totals.index, y=category_totals.values, palette="coolwarm")
    plt.title("Total Purchases per Category")
    plt.xlabel("Category")
    plt.ylabel("Total Purchase Amount")

    # Barplot for average purchase per gender
    plt.subplot(1, 3, 2)
    sns.barplot(x=avg_purchase_gender.index, y=avg_purchase_gender.values, palette="muted")
    plt.title("Avg Purchase Amount by Gender")
    plt.xlabel("Gender")
    plt.ylabel("Avg Purchase Amount")

    # Barplot for average purchase by age group
    plt.subplot(1, 3, 3)
    sns.barplot(x=age_group_avg.index, y=age_group_avg.values, palette="viridis")
    plt.title("Avg Purchase Amount by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Avg Purchase Amount")

    plt.tight_layout()
    
    # Save the plot
    if not os.path.exists("static"):
        os.makedirs("static")
    plt.savefig("static/plot.png")
    plt.close()

@app.route("/")
def home():
    save_plot()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)