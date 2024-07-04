import pandas as pd
import psycopg2


def db_conn():
    try:
        conn = psycopg2.connect(database="toiletDB", host="localhost", user="postgres", password="Pass@word1", port=5432)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


df = pd.read_csv("toilet.csv")
for column in df.columns:
    df[column] = df[column].str.strip()

data_dict = df.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
df_location = pd.read_csv("Location.csv")
location_dict = df_location.to_dict(orient='records')

con = db_conn()
if con is not None:
    try:
        cur = con.cursor()
        insert_query = """
        INSERT INTO tbltoilet(
            lavatoryid, description, city, street, isopen24hours, postalcode, location, country,
            longitude, latitude, price, isownedbywall, ishandicappedaccessible,
            canbepayedwithcoins, canbepayedinapp, canbepayedwithnfc, haschangingtable,
            hasurinal, labelid, fid)
        VALUES (
            %(LavatoryID)s, %(Description)s, %(City)s, %(Street)s, %(IsOpen24Hours)s,
            %(PostalCode)s, %(Location)s, %(Country)s, %(Longitude)s, %(Latitude)s, %(Price)s,
            %(isOwnedByWall)s, %(isHandicappedAccessible)s,  %(canBePayedWithCoins)s,
            %(canBePayedInApp)s, %(canBePayedWithNFC)s, %(hasChangingTable)s,
            %(hasUrinal)s, %(LabelID)s, %(FID)s)
        """
        insert_location = """
        INSERT INTO tbllocation(
            location, longitude, latitude)
        VALUES(
        %(Location)s, %(Longitude)s, %(Latitude)s)
        """

        cur.executemany(insert_location, location_dict)
        con.commit()
        cur.close()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        con.close()
else:
    print("Connection to database failed")
