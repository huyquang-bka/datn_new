import sqlite3
import pandas as pd
import random
from tqdm import tqdm

conn = sqlite3.connect("traffic.db")
cursor = conn.cursor()
# print all columns
# df = pd.read_sql_query(con=conn, sql="SELECT * FROM traffic")
# print(df.head())
# print(df.describe())
command = "drop table traffic"
cursor.execute(command)
conn.commit()
command = "CREATE TABLE traffic (date text, time text, car integer, motorbike integer)"
cursor.execute(command)
conn.commit()
df = pd.DataFrame(columns=["date", "time", "car", "motorbike"])
for date in pd.date_range("2023-01-05", "2023-01-06"):
    date = date.strftime("%Y-%m-%d")
    print(date)
    car = 0
    motorbike = 0
    for time in tqdm(pd.date_range("00:00:00", "23:59:59", freq="1s")):
        time = time.strftime("%H:%M:%S")
        car = random.randint(0, 2)
        motorbike = random.randint(0, 3)
        # command = f"INSERT INTO traffic (date, time, car, motorbike) VALUES ('{date}', '{time}', 0, 0)"
        df = pd.concat([df, pd.DataFrame([[date, time, car, motorbike]], columns=[
                       "date", "time", "car", "motorbike"])])
# cursor.execute(command)
# conn.commit()
df.to_sql("traffic", conn, if_exists="replace", index=False)
print(df.head())
