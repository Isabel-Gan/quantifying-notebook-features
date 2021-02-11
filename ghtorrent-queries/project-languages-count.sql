SELECT 
	language, COUNT(*) as count 
FROM 
	`ghtorrent-2019-06`.projects
WHERE
	deleted = 0 
GROUP BY language
ORDER BY count DESC