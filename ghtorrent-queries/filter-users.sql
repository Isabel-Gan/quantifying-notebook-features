SELECT 
	id, login, created_at 
FROM
	`ghtorrent-2019-06`.users
WHERE
	deleted = 0 AND fake = 0