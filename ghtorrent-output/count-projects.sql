SELECT 
	owner_id, COUNT(*) as count 
FROM 
	`ghtorrent-2019-06`.projects
WHERE
	deleted = 0 AND 
    LANGUAGE = 'C'
GROUP BY owner_id 
ORDER BY count DESC