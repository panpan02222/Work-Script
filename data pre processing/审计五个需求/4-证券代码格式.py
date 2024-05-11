import pandas as pd

df = pd.read_excel('merged_data_with_additional_info.xlsx')

df['证券代码'] = df['证券代码'].astype(str).str.zfill(6)

df.to_excel('merged_data_with_additional_info_filled_code.xlsx', index=False)
