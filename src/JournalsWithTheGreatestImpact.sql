use p5g1;

-- Journals with the Greatest Impact

SELECT 
    J.JournalID,
    J.[Name] AS JournalName,
    YEAR(V.PublicationDate) AS PublicationYear,
    COUNT(C.CitingArticleID) AS TotalCitations
FROM 
    Journal J
    JOIN JournalVolume V ON J.JournalID = V.JournalID
    JOIN Article A ON V.JournalID = A.JournalID AND V.Volume = A.Volume
    LEFT JOIN Cited_by C ON A.ArticleID = C.CitedArticleID
GROUP BY 
    J.JournalID,
    J.[Name],
    YEAR(V.PublicationDate)
ORDER BY 
    PublicationYear,
    TotalCitations DESC;
