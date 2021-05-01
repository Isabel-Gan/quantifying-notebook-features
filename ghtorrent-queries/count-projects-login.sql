SELECT C.owner_id, U.login, U.type, C.cnt
FROM (SELECT owner_id, count(owner_id) as cnt 
		FROM `ghtorrent-2019-06`.projects
        WHERE deleted = 0 AND 
				forked_from IS NULL AND 
				(language = 'Jupyter Notebook' OR 
				language = 'R')
        GROUP BY owner_id) C
INNER JOIN `ghtorrent-2019-06`.users U ON U.id = C.owner_id
WHERE U.type = 'USR'
ORDER BY C.cnt DESC