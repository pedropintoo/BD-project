use p5g1;

--MostProductiveAuthorsByTopic

SELECT 
    T.TopicID,
    T.[Name] AS TopicName,
    A.AuthorID,
    A.[Name] AS AuthorName,
    TopicAuthorCounts.ArticlesCount
FROM 
    Topic T
    JOIN (
        SELECT 
            B.TopicID,
            W.AuthorID,
            COUNT(W.ArticleID) AS ArticlesCount,
            ROW_NUMBER() OVER (PARTITION BY B.TopicID ORDER BY COUNT(W.ArticleID) DESC, A.[Name]) AS AuthorRank
        FROM 
            Belongs_to B
            JOIN Article R ON B.ArticleID = R.ArticleID
            JOIN Wrote_by W ON R.ArticleID = W.ArticleID
            JOIN Author A ON W.AuthorID = A.AuthorID
        GROUP BY 
            B.TopicID, W.AuthorID, A.[Name]
    ) AS TopicAuthorCounts ON T.TopicID = TopicAuthorCounts.TopicID
    JOIN Author A ON TopicAuthorCounts.AuthorID = A.AuthorID
WHERE 
    TopicAuthorCounts.AuthorRank = 1
ORDER BY 
    T.TopicID;






