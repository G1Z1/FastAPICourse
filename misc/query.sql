SELECT posts.*, COUNT(votes.post_id) AS votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id WHERE posts.id = 10
SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at, posts.owner_id AS posts_owner_id 
FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id
SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at, posts.owner_id AS posts_owner_id, count(votes.post_id) AS votes
FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id GROUP BY posts.id