# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import pymysql as db
import settings
import sys

def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        settings.mysql_host, 
        settings.mysql_user, 
        settings.mysql_passwd, 
        settings.mysql_schema)
    
    return con

def updateRank(rank1, rank2, movieTitle):

    # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()

    try:
        float(rank1)
    except ValueError:
        return [("status",),("error",),]
    try:
        float(rank2)
    except ValueError:
        return [("status",),("error",),]
    
    if float(rank1)<0.0  or float(rank1)>10.0 or float(rank2)<0.0 or float(rank2)>10.0:
    	db.close()
    	return [("status",),("error",),]
    sql1="SELECT movie_id FROM movie WHERE movie.title= %s"
    cur.execute(sql1,(movieTitle,))
    rows=cur.fetchall()
    if len(rows)==0 or len(rows)>1:
    	con.close()
    	return [("status",),("error",),]
    else:
    	sql2="SELECT movie_id FROM movie WHERE movie.title=%s AND movie.rank IS NULL"
    	cur.execute(sql2,(movieTitle,))
    	plithos=cur.fetchone()
    	if plithos is not None:
    		mo=(rank1+rank2)/2
    		sql3="UPDATE movie SET movie.rank=%s WHERE movie.title=%s"
    		arg=(mo,movieTitle)
    		cur.execute(sql3,arg)
    		con.commit()
    	else:
    		cur.execute("SELECT * FROM movie WHERE movie.title= %s",(movieTitle,))
    		val=cur.fetchall()
    		for row in val:
    			rank=row[3]
    		var=float(rank)
    		rank1=float(rank1)
    		rank2=float(rank2)
    		mo=(var+rank1+rank2)/3
    		arg=(mo,movieTitle)
    		cur.execute("UPDATE movie SET movie.rank=%s WHERE movie.title=%s",arg)
    		con.commit()
    	con.close()
    return [("status",),("ok",),]


def colleaguesOfColleagues(actorId1, actorId2):

    # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
 
    l1=list()
    l2=list()
    actorID1=(actorId1,actorId1,)
    actorID2=(actorId2,actorId2,)
    sql="SELECT DISTINCT  actor.actor_id FROM actor \
    INNER JOIN role on role.actor_id=actor.actor_id AND actor.actor_id!= %s\
    WHERE role.movie_id in (SELECT DISTINCT  movie.movie_id FROM movie,role,actor\
    WHERE role.movie_id=movie.movie_id AND role.actor_id=%s)"
    sql2="SELECT  distinct(movie.title)  from movie,role r1,role r2\
	WHERE  r1.actor_id=%s and r2.actor_id=%s  and r1.actor_id!=r2.actor_id and r2.movie_id=r1.movie_id and r1.movie_id=movie.movie_id"

    cur.execute(sql,actorID1)
    results1=cur.fetchall()
    for row in results1:
    	l1.append(row[0])
    cur.execute(sql,actorID2)
    results2=cur.fetchall()
    for row in results2:
    	l2.append(row[0])
    

    list1=list()
    list2=list()
    list3=list()
    list4=list()
    list5=list()
    
    if len(l2)<=len(l1):
 	    for i in l1:
 		    for j in l2:
 			    arg1=(i,j,) 
 			    cur.execute(sql2,arg1)
 			    re=cur.fetchall()
 			    if re:
 			    	for row in re:
 			    		list1.append(str(row[0]))
 			    		list2.append(int(i))
 			    		list3.append(int(j))
 			    		list4.append(int(actorId1))
 			    		list5.append(int(actorId2))
    else:
 	    for i in l2:
 		    for j in l1:
 			    arg1=(i,j,)
 			    cur.execute(sql2,arg1)
 			    re=cur.fetchall()
 			    if re:
 			    	for row in re:
 			    		list1.append(str(row[0]))
 			    		list2.append(int(i))
 			    		list3.append(int(j))
 			    		list4.append(int(actorId1))
 			    		list5.append(int(actorId2))
 			    	
    con.close()
    Mega_List=list()
    for  i in range(len(list1)):
    		re=(list1[i],list2[i],list3[i],list4[i],list5[i])
    		Mega_List.append(re)
    Final_Apotelesma=[("movieTitle","collagueofActor1","collagueofActor2","actor1","actor2",)]
    Final_Apotelesma.extend(Mega_List)
    return Mega_List


def actorPairs(actorId):

    # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
	
	
    Mega_List=list()
    sql="SELECT distinct actor.actor_id FROM actor,role,movie_has_genre \
    WHERE actor.actor_id=role.actor_id AND role.movie_id=movie_has_genre.movie_id AND movie_has_genre.genre_id NOT IN (\
    SELECT distinct movie_has_genre.genre_id from movie_has_genre,actor,role\
    WHERE movie_has_genre.movie_id=role.movie_id and role.actor_id=%s)\
    ORDER BY actor.actor_id"

    sql2="SELECT DISTINCT mg1.genre_id FROM movie_has_genre mg1,role r1\
	WHERE r1.actor_id=%s and r1.movie_id=mg1.movie_id\
	order by mg1.genre_id"


    cur.execute(sql,(actorId,))
    result=cur.fetchall()
    my_list=[]
    for row in result:
    	my_list.append(row[0])

    
    re1=list()
    cur.execute(sql2,(actorId,))
    re=cur.fetchall()
    for row in re:
    	re1.append(row[0])


    re2=list()
    e=list()
    for x in my_list:
    	re2=[]
    	not_all=0
    	e=[]
    	arg=(x,)
    	cur.execute(sql2,arg)
    	apo=cur.fetchall()
    	for row in apo:
    		re2.append(row[0])
    	for i in re2:
    		for j in re1:
    			if i==j:
    				not_all=1
    	if not_all==1:
    		continue
    	e.extend(re1)
    	e.extend(val for val in re2 if val not in re1)
    	if len(e)>=7:
    		Mega_List.append(x)
 		

    con.close()
    Telos=list()
    for i in range(len(Mega_List)):
    	re=(Mega_List[i])
    	re=(re,)
    	Telos.append(re)
    Final_Apotelesma=[("actorId2",)]
    Final_Apotelesma.extend(Telos)
    Final_Apotelesma=tuple(Final_Apotelesma)
    return Final_Apotelesma
    
    return [("actor2Id",),]
	
def selectTopNactors(n):

    # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    MegaList=list()
    Mega1=list()
    Mega2=list()
    print(type(n))
    Mega3=list()
    list1=list()
    list2=list()
    list3=list()
    sql1="SELECT  genre_id FROM genre"
    sql3="SELECT COUNT(*) FROM genre"
    sql2="SELECT  genre.genre_name,actor.actor_id,count(movie_has_genre.movie_id)\
	FROM actor,role,movie_has_genre,genre\
	WHERE movie_has_genre.genre_id=%s AND movie_has_genre.genre_id=genre.genre_id AND movie_has_genre.movie_id=role.movie_id AND role.actor_id=actor.actor_id \
	GROUP BY actor.actor_id\
	ORDER BY count(movie_has_genre.movie_id) DESC"
    cur.execute(sql1,)
    re=cur.fetchall()
    mylist=list()
    mylist1=list()
    for i in re:
    	mylist.append(i)

    for i in mylist:
    	cur.execute(sql2,(i,))
    	apo=cur.fetchall()
    	for row in apo:
    		list1.append(str(row[0]))
    		list2.append(int(row[1]))
    		list3.append(int(row[2]))

    	if len(list1)>int(n):
    		for j in range(0,int(n)):
    			q=(list1[j],list2[j],list3[j])
    			MegaList.append(q)
    	else:
    		for h in range(len(list1)):
    			q=(list1[h],list2[h],list3[h])
    			MegaList.append(q)
    	list1=[]
    	list2=[]
    	list3=[]
   
    Final_Apotelesma=[("genreName", "actorId", "numberOfMovies"),]
    Final_Apotelesma.extend(MegaList)
    return Final_Apotelesma
