import pandas as pd
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

def analysis(df):
    # Now we can do some analysis on the data set
    print("Delivery days average by shipping mode:")
    Ship=df.groupby("Ship-Mode").agg({"Delivery_Days":"mean"})
    print(Ship)

    print("Top 5 sub categories by sales:")
    print(df.groupby("Sub-Category")[["Sales","Profit"]].sum().sort_values("Sales", ascending=False).head(5))

    print("Sales and profits by month:")
    year_profit=df.groupby(["Year", "Month"]).agg({"Sales":"sum","Profit":"sum"})
    print(year_profit)

    print("Region wise profits:")
    reason_Profit=df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
    print(reason_Profit)

    # Insight: The meaningful data retrieved from analysis of the data set
    print('Insights from the analysis:')
    print(f"{reason_Profit.idxmax()} Region have  maximum profit, Strong sales and good customer base")
    print(f"{reason_Profit.idxmin()} Region have  minimum profit, Weak sales and poor customer base")

    peak_year, peak_month = year_profit["Sales"].idxmax()
    print(f"Maximum sales happened in Year {peak_year}, Month {peak_month}")

    print(f"{Ship.idxmin()} is the fastest shipping mode")
    print(f"{Ship.idxmax()} is the slowest shipping mode")

def main():
    if len(sys.argv)<2:
        print("Please provide the file path as an argument")
        sys.exit(1)
    file_path=sys.argv[1]
    data=load_data(file_path)
    basic_info(data)
    data=handling_data(data)
    data=convert_data_types(data)
    print("Final data types after conversion are:")
    print(data.dtypes)
    
    # Now lets add new columns for month, year and delay in shipping for further analysis
    data=feature_engineering(data)
    # Now we can do some analysis on the data set
    analysis(data)
if __name__=="__main__":    main()