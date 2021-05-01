SELECT 
	user_id, COUNT(*) as count 
FROM 
	`ghtorrent-2019-06`.followers
GROUP BY user_id 
ORDER BY count DESC