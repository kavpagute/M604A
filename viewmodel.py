import psycopg2
con = psycopg2.connect(database="toiletDB", host="localhost", user="postgres", password="Pass@word1", port=5432)
cur = con.cursor()
sql_handicapped = "CREATE VIEW Vhandicapped\
       AS SELECT location, count(*) FILTER (WHERE ishandicappedaccessible = true) AS hc_true\
       FROM tbltoilet\
       GROUP BY location\
       ORDER BY (count(*) FILTER (WHERE ishandicappedaccessible = true)) DESC;"
cur.execute(sql_handicapped)
sql_vfreetoilet = "CREATE VIEW Vfreetoilet\
        AS select location, count(price) as free_toilet from tbltoilet where price=0::money\
        group by location order by free_toilet desc;"
cur.execute(sql_vfreetoilet)
sql_open24hours = "CREATE VIEW public.visopen24hours AS\
        SELECT tt.location, count(tt.location) as open24hours FROM tbltoilet as tt\
	    left join tbllocation as tl on tt.location=tl.location\
        where tt.isopen24hours='Yes'\
        group by tt.location\
        order by open24hours desc;"
cur.execute(sql_open24hours)
con.commit()
con.close()

