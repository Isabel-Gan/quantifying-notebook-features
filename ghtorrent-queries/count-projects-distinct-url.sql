SELECT C.owner_id, U.login, U.type, C.cnt
FROM (SELECT owner_id, count(owner_id) as cnt
		FROM (SELECT min(owner_id) as owner_id, 
						min(language) as language, 
                        min(forked_from) as forked_from, 
                        min(deleted) as deleted, url 
				FROM `ghtorrent-2019-06`.projects 
				GROUP BY url
                LIMIT 50000) CC
		WHERE 
			CC.deleted = 0 AND 
			CC.forked_from IS NULL 
		GROUP BY CC.owner_id
        LIMIT 100) C
INNER JOIN `ghtorrent-2019-06`.users U ON U.id = C.owner_id
ORDER BY C.cnt DESC
        

