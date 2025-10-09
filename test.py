import pandas as pd

pbp = pd.read_parquet("pbp_2024.parquet")
# If you only saved CSV: pbp = pd.read_csv("pbp_2024.csv")

fourth = pbp[pbp["down"] == 4].copy()
print(fourth.head())
print("rows:", len(fourth))
print(fourth["play_type"].value_counts())


