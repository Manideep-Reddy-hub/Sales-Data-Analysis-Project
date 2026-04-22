import pandas as pd
import matplotlib.pyplot as plt
import sys
def load_data(file_path):
    try:
        data=pd.read_csv(file_path, encoding='latin1')
        return data
    except Exception as e:
        print("Error in the loading the data",e)
        sys.exit(1)

def clean_data(df):
    df['Postal Code']=df['Postal Code'].fillna(0).astype(int)
    return df

def missing_values(df):
    print("Missing values in the data set is:")
    print(df.isnull().sum())

def handling_data(df):
    missing_values(df)
    df=clean_data(df)
    print("After cleaning the data the missing values in the data sets")
    missing_values(df)
    return df

def convert_data_types(df):
    df['Order-Date']=pd.to_datetime(df['Order-Date'])
    df["Ship-Date"]=pd.to_datetime(df["Ship-Date"])
    df["Category"]=df["Category"].astype("category")
    return df

def basic_info(df):
    print("Row and columns of the data set is:",df.shape)
    print("Statistical summary of the data set is:")
    print(df.describe())

def feature_engineering(df):
    df['Month']=df['Order-Date'].dt.month
    df['Year']=df['Order-Date'].dt.year
    df["Delivery_Days"]=(df["Ship-Date"]-df["Order-Date"]).dt.days
    return df

def combine_plot(df):
    plt.figure(figsize=(14,18))
    
    plt.subplot(3,1,1)
    sale_profit=df.groupby("Sub-Category")[["Sales","Profit"]].sum().sort_values("Sales", ascending=False)
    sub_category=sale_profit.index.tolist()
    sales=sale_profit["Sales"].tolist()
    profit=sale_profit["Profit"].tolist()
    profit_color=[ 'red' if x<0 else 'orange' for x in profit]
    x = range(len(sub_category))
    plt.bar([i - 0.2 for i in x], sales, width=0.4, color='blue')
    plt.bar([i + 0.2 for i in x], profit, width=0.4, color=profit_color)
    plt.title("Sales and Profit of Sub-Category")
    plt.xlabel("Sub-Category")
    plt.ylabel("Amount")
    plt.xticks(x, sub_category, rotation=60,ha='right')
    plt.legend(["Sales", "Profit"])
    
    plt.subplot(3,1,2)
    reason_Profit=df.groupby("Region")[["Sales","Profit"]].sum().sort_values("Sales", ascending=False)
    region=reason_Profit.index.tolist()
    sales_region=reason_Profit["Sales"].tolist()
    profit_region=reason_Profit["Profit"].tolist()
    x = range(len(region))
    plt.bar([i - 0.2 for i in x], sales_region, width=0.4, color='green')#sales by region shifted to left by 0.2
    plt.bar([i + 0.2 for i in x], profit_region, width=0.4, color='yellow') #profit by region shifted to right by 0.2
    plt.title("Sales and Profit by Region")
    plt.xlabel("Region")
    plt.ylabel("Amount")
    plt.xticks(x, region, rotation=45, ha='right') #ha is horizontal alignment of the x-axis labels
    plt.legend(["Sales", "Profit"])

    plt.subplot(3,1,3)
    Ship=df.groupby("Ship-Mode")[ "Delivery_Days"].mean().sort_values()
    ship_mode=Ship.index.tolist()
    delivery_days=Ship.tolist()
    x = range(len(ship_mode))
    plt.bar(x,delivery_days, color='purple')
    plt.title("Average Delivery Days by Shipping Mode")
    plt.xlabel("Shipping Mode")
    plt.ylabel("Average Delivery Days")
    plt.xticks(x, ship_mode, rotation=0, ha='right')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.8)# Adjust the vertical spacing between subplots
    plt.show()
def analysis(df):
    # Now we can do some analysis on the data set
    print("Delivery days average by shipping mode:")
    Ship=df.groupby("Ship-Mode")[ "Delivery_Days"].mean().sort_values()
    print(Ship)

    print("Top 5 sub categories by sales:")
    rev=df.groupby("Sub-Category")[["Sales","Profit"]].sum().sort_values("Sales", ascending=False)
    print(rev.head(5))

    print("Sales and profits by month:")
    year_profit=df.groupby(["Year", "Month"]).agg({"Sales":"sum","Profit":"sum"})
    print(year_profit)

    print("Region wise profits:")
    reason_Profit=df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
    print(reason_Profit)

    region_margin = (reason_Profit / df.groupby("Region")["Sales"].sum()).sort_values(ascending=False)
    print("Region wise profit margin:")
    print(region_margin)
    # Insight: The meaningful data retrieved from analysis of the data set
    print('Insights from the analysis:')
    loss_products=rev[rev['Profit']<0].index.tolist()
    print(f"Loss products are: {loss_products}")#loss products names will be displayed
    print("Pricing or discount issue detected.\n")

    print(f"{reason_Profit.idxmax()} Region generates the highest profit")
    print("Strong market, focus investment here.\n")
    print(f"{reason_Profit.idxmin()} Region generates the  lowest profit")
    print("Weak market, consider strategies to improve performance.\n")


    peak_year, peak_month = year_profit["Sales"].idxmax()
    print(f"Maximum sales happened in Year {peak_year}, Month {peak_month}")

    print(f"{Ship.idxmin()} is the fastest shipping mode")
    print("This is the most efficient shipping mode and the company should consider using it more for best customer satisfaction")
    print(f"{Ship.idxmax()} is the slowest shipping mode")
    print("This is the slowest shipping mode and the company need to improve the logistics")

def conclusion():
    print("\nFinal Business Conclusion:")
    print("1. Focus on high-performing regions to maximize revenue.")
    print("2. Review pricing strategy for loss-making products.")
    print("3. Improve slow shipping modes to enhance customer satisfaction.")
    print("4. Leverage seasonal trends to plan inventory and marketing.")
def main():
    if len(sys.argv)<2:
        print("Please provide the file path as an argument")
        sys.exit(1)
    file_path=sys.argv[1]
    data=load_data(file_path)
    print("Analyzing Superstore sales data to identify profitability and operational insights...\n")
    print("The columns in the data set are:",data.columns.tolist())
    basic_info(data)
    data=handling_data(data)
    data=convert_data_types(data)
    print("Final data types after conversion are:")
    print(data.dtypes)
    
    # Now lets add new columns for month, year and delay in shipping for further analysis
    data=feature_engineering(data)
    # Now we can do some analysis on the data set
    analysis(data)
    combine_plot(data)
    conclusion()
    
if __name__=="__main__":    main()