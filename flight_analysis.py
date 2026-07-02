# ================================================
# SCRIPT 1 — Split flights.csv into 6 parts
# ================================================

import pandas as pd
import os

file = r'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/flights.csv'
save_folder = r'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads'

df = pd.read_csv(file)
print(f'Total rows: {len(df)}')

chunk_size = 1000000
for i, start in enumerate(range(0, len(df), chunk_size)):
    chunk = df[start : start + chunk_size]
    filename = os.path.join(save_folder, f'flights_part{i+1}.csv')
    chunk.to_csv(filename, index=False)
    print(f'Part {i+1} saved — {len(chunk)} rows')

# ================================================
# SCRIPT 2 — Load parts into flights_staging
# ================================================

import mysql.connector
DB_PASSWORD = 'Abhi@100982'

# Connect to MySQL
conn = mysql.connector.connect(
    host     = 'localhost',
    user     = 'root',           
    password = 'DB_PASSWORD',  
    database = 'airline_performance',
    allow_local_infile = True
)
cursor = conn.cursor()

# Enable local infile on server
cursor.execute("SET GLOBAL local_infile = 1")

parts = [
    r'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/flights_part1.csv',
    r'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/flights_part2.csv',
    r'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/flights_part3.csv',
    r'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/flights_part4.csv',
    r'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/flights_part5.csv',
    r'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/flights_part6.csv',
]

for part in parts:
    print(f'Loading {part} ...')
    sql = f"""
        LOAD DATA LOCAL INFILE '{part}' INTO TABLE flights_staging FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\\n' IGNORE 1 ROWS
    """
    cursor.execute(sql)
    conn.commit()
    print(f'Done — {cursor.rowcount} rows inserted')

# Final check
cursor.execute('SELECT COUNT(*) FROM flights_staging')
print(f'\n Total rows: {cursor.fetchone()[0]}')

cursor.close()
conn.close()

# ================================================
# SCRIPT 3 — INSERT staging into flights table
# ================================================

import mysql.connector

conn = mysql.connector.connect(
    host     = 'localhost',
    user     = 'root',
    password = 'DB_PASSWORD',
    database = 'airline_performance'
)
cursor = conn.cursor()

print("Starting INSERT from staging to flights...")

cursor.execute("SET sql_mode = ''")

cursor.execute("""
    INSERT INTO flights
    SELECT
        NULLIF(TRIM(YEAR),''),                NULLIF(TRIM(MONTH),''),
        NULLIF(TRIM(DAY),''),                 NULLIF(TRIM(DAY_OF_WEEK),''),
        NULLIF(TRIM(AIRLINE),''),             NULLIF(TRIM(FLIGHT_NUMBER),''),
        NULLIF(TRIM(TAIL_NUMBER),''),         NULLIF(TRIM(ORIGIN_AIRPORT),''),
        NULLIF(TRIM(DESTINATION_AIRPORT),''), NULLIF(TRIM(SCHEDULED_DEPARTURE),''),
        NULLIF(TRIM(DEPARTURE_TIME),''),      NULLIF(TRIM(DEPARTURE_DELAY),''),
        NULLIF(TRIM(TAXI_OUT),''),            NULLIF(TRIM(WHEELS_OFF),''),
        NULLIF(TRIM(SCHEDULED_TIME),''),      NULLIF(TRIM(ELAPSED_TIME),''),
        NULLIF(TRIM(AIR_TIME),''),            NULLIF(TRIM(DISTANCE),''),
        NULLIF(TRIM(WHEELS_ON),''),           NULLIF(TRIM(TAXI_IN),''),
        NULLIF(TRIM(SCHEDULED_ARRIVAL),''),   NULLIF(TRIM(ARRIVAL_TIME),''),
        NULLIF(TRIM(ARRIVAL_DELAY),''),       NULLIF(TRIM(DIVERTED),''),
        NULLIF(TRIM(CANCELLED),''),           NULLIF(TRIM(CANCELLATION_REASON),''),
        NULLIF(TRIM(AIR_SYSTEM_DELAY),''),    NULLIF(TRIM(SECURITY_DELAY),''),
        NULLIF(TRIM(AIRLINE_DELAY),''),       NULLIF(TRIM(LATE_AIRCRAFT_DELAY),''),
        NULLIF(TRIM(WEATHER_DELAY),'')
    FROM flights_staging
""")

conn.commit()
print("INSERT complete - " + str(cursor.rowcount) + " rows inserted")

cursor.execute("SET sql_mode = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION'")

cursor.execute("SELECT COUNT(*) FROM flights")
print("Total rows in flights table: " + str(cursor.fetchone()[0]))

cursor.close()
conn.close()

# ================================================
# SCRIPT 4 — Verify row count
# ================================================

import mysql.connector

conn = mysql.connector.connect(
    host     = 'localhost',
    user     = 'root',
    password = 'DB_PASSWORD',
    database = 'airline_performance'
)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM flights")
print("Total rows in flights: " + str(cursor.fetchone()[0]))
cursor.close()
conn.close()

# ================================================
# SCRIPT 5 — Update FLIGHT_DATE column
# ================================================

import mysql.connector

conn = mysql.connector.connect(
    host     = 'localhost',
    user     = 'root',
    password = 'DB_PASSWORD',
    database = 'airline_performance',
    connection_timeout = 3600
)

# Increase timeout at session level
conn.cmd_query('SET SESSION wait_timeout = 28800')
conn.cmd_query('SET SESSION interactive_timeout = 28800')
conn.cmd_query('SET SESSION net_read_timeout = 3600')
conn.cmd_query('SET SESSION net_write_timeout = 3600')
conn.cmd_query('SET SQL_SAFE_UPDATES = 0')

cursor = conn.cursor()

print("Updating FLIGHT_DATE column...")

cursor.execute("""
    UPDATE flights
    SET FLIGHT_DATE = STR_TO_DATE(
        CONCAT(YEAR, '-',
               LPAD(MONTH, 2, '0'), '-',
               LPAD(DAY,   2, '0')),
        '%Y-%m-%d'
    )
""")

conn.commit()
print("Done - " + str(cursor.rowcount) + " rows updated")

# Verify
cursor.execute("SELECT YEAR, MONTH, DAY, FLIGHT_DATE FROM flights LIMIT 5")
rows = cursor.fetchall()
print("\nSample verification:")
print("YEAR  MONTH  DAY  FLIGHT_DATE")
print("-" * 35)
for row in rows:
    print(str(row[0]) + "    " + str(row[1]) + "      " + str(row[2]) + "    " + str(row[3]))

cursor.close()
conn.close()
