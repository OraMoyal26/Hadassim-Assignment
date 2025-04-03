import pandas as pd




def read_file(file_path):
  if file_path[-4:]=="xlsx":
    df= pd.read_excel(file_path)
  elif file_path[-3:]=="csv":
    df= pd.read_csv(file_path)
  elif file_path[-7:]=="parquet":
    df= pd.read_parquet(file_path, columns=["timestamp", "value"])
  return df



def clean_data(df):
  df['timestamp']= pd.to_datetime(df['timestamp'], errors='coerce')
  df['value']= pd.to_numeric(df['value'], errors='coerce')
  df= df.dropna()
  df=df.drop_duplicates(subset=['timestamp'], keep='first')
  return df


def mean_fer_hour_in_day(df):
  df.loc[:, 'start_time']= df['timestamp'].dt.floor('h')
  return df[["start_time", "value"]].groupby('start_time').mean()



def mean_fer_hour_in_all_days(df):
  df["date"]= df['timestamp'].dt.date
  df_dates=[]

  for d in df["date"].unique():
    df_dates.append(mean_fer_hour_in_day(df[df["date"]==d]))

  return(pd.concat(df_dates))




def mean_fer_hour(file_path):
  df= read_file(file_path)
  df= clean_data(df)
  return(mean_fer_hour_in_all_days(df))





if __name__ == "__main__":
  file_path= "time_series.xlsx"
  df= mean_fer_hour(file_path)
  df.sort_values(by='start_time')
  df['value']= df['value'].round(3)

  path_to_result= "mean_fer_hour.csv"
  df.to_csv(path_to_result, header=True)

