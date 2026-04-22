import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv("superstore.csv", encoding='latin1')

data2=data.groupby("Sub-Category")[["Sales","Profit"]].sum().sort_values("Sales", ascending=False)