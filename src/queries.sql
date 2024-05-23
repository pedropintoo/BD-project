SELECT PublicationYear, [Name], T.rank_pub
FROM (
	SELECT COUNT(Topic.TopicID) AS TopicCount, Topic.[Name], RANK() OVER (PARTITION BY YEAR(PublicationDate) ORDER BY COUNT(Topic.TopicID) DESC, [Name]) AS rank_pub, YEAR(PublicationDate) AS PublicationYear
	FROM Topic
	INNER JOIN Belongs_to ON Belongs_to.TopicID = Topic.TopicID
	INNER JOIN Article ON Article.ArticleID = Belongs_to.ArticleID
	INNER JOIN JournalVolume ON JournalVolume.JournalID = Article.JournalID
	GROUP BY Topic.[Name], YEAR(PublicationDate)
) AS T
WHERE T.rank_pub BETWEEN 1 AND 3
ORDER BY T.PublicationYear DESC, T.rank_pub