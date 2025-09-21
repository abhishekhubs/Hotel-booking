import pandas as pd
import matplotlib.pyplot as plt
files = {
    "Bangalore": "bangalore.csv",
    "Delhi": "delhi.csv",
    "Hyderabad": "hyderabad.csv",
    "Kolkata": "kolkata.csv",
    "Mumbai": "mumbai.csv",
}

dfs = []
for city, path in files.items():
    df = pd.read_csv(path)
    df["City"] = city
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)                

# Clean price column
data["Price"] = data["Price"].astype(str).str.replace(",", "").astype(float)
avg_price_city_room = (
    data.groupby(["City", "Star Rating"])["Price"]
    .mean()
    .reset_index()
)

print("\nAverage Price per City & Room Type:")
print(avg_price_city_room)

plt.figure(figsize=(10,6))
cities = data["City"].unique()
for i, city in enumerate(cities):
    subset = avg_price_city_room[avg_price_city_room["City"] == city]
    plt.bar(
        subset["Star Rating"] + i*0.15,
        subset["Price"],
        width=0.15,
        label=city
    )

plt.xlabel("Star Rating (Room Type Proxy)")
plt.ylabel("Average Price (INR)")
plt.title("Average Hotel Price per City by Room Type")
plt.legend()
plt.show()

busiest_city = (
    data.groupby("City")["Reviews"]
    .sum()
    .reset_index()
    .sort_values(by="Reviews", ascending=False)
)
plt.figure(figsize=(8,8))
plt.pie(busiest_city["Reviews"], labels=busiest_city["City"], autopct='%1.1f%%', startangle=140)
plt.title("Busiest Cities by Total Reviews (Demand Proxy)")
plt.show()
print("\nBusiest Cities by Total Reviews:")
print(busiest_city)
print("\nTop 10 Hotels by Reviews (Popularity Ranking):")
for city in data["City"].unique():
    print(f"\n🏙️ {city}:")
    top_hotels = data[data["City"] == city].sort_values(by="Reviews", ascending=False).head(10)
    print(top_hotels[["Hotel Name", "Reviews", "Price", "Star Rating"]])
plt.figure(figsize=(12,6))
for city in data["City"].unique():
    subset = data[data["City"] == city]
    plt.hist(subset["Price"], bins=30, alpha=0.5, label=city)

plt.xlabel("Price (INR)")
plt.ylabel("Number of Hotels")
plt.title("Price Distribution of Hotels per City")
plt.legend()
plt.show()
# Boxplot
plt.figure(figsize=(10,6))
data.boxplot(column="Price", by="City", grid=False)
plt.xlabel("City")
plt.ylabel("Price (INR)")
plt.title("Hotel Price Spread per City")
plt.show()
# Price vs Reviews
plt.figure(figsize=(10,6))
for city in cities:
    subset = data[data["City"] == city]
    plt.scatter(subset["Reviews"], subset["Price"], alpha=0.6, label=city)
plt.xlabel("Number of Reviews (Demand Proxy)")
plt.ylabel("Price (INR)")
plt.title("Hotel Price vs Demand (Reviews) by City")
plt.legend()
plt.show()
# Price vs Star Rating
plt.figure(figsize=(10,6))
for city in cities:
    subset = data[data["City"] == city]
    plt.scatter(subset["Star Rating"], subset["Price"], alpha=0.6, label=city)
plt.xlabel("Star Rating")
plt.ylabel("Price (INR)")
plt.title("Hotel Price vs Star Rating by City")
plt.legend()
plt.show()
