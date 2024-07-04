import psycopg2
con = psycopg2.connect(database="toiletDB", host="localhost", user="postgres", password="Pass@word1", port=5432)
cur = con.cursor()
sql_table = "CREATE TABLE tbltoilet(toiletid integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ), PRIMARY KEY(toiletid), \
    lavatoryid character varying(20),\
    description character varying(150),\
    city character varying(10),\
    street character varying(100),\
    isopen24hours character varying(10),\
    postalcode integer,\
    location character varying(150),\
    country character varying(20),\
    longitude real,\
    latitude real,\
    isownedbywall boolean,\
    ishandicappedaccessible boolean,\
    price money,\
    canbepayedwithcoins boolean,\
    canbepayedinapp boolean,\
    canbepayedwithnfc boolean,\
    haschangingtable boolean,\
    labelid integer,\
    hasurinal boolean,\
    fid integer)"
cur.execute(sql_table)
sql_location = ("CREATE TABLE tbllocation(locationid integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ), "
                "PRIMARY KEY(locationid), \
    location character varying(150),\
    longitude real,\
    latitude real)")
cur.execute(sql_location)
con.commit()
con.close()





