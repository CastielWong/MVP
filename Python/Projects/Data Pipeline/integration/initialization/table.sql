
USE [DataPipeline]

IF NOT EXISTS (
    SELECT  *
    FROM sys.tables t
        JOIN sys.schemas s ON (t.schema_id = s.schema_id)
    WHERE s.name = 'dbo' AND t.name = 'apple'
)
    BEGIN
        CREATE TABLE [dbo].[apple] (
            [source_date]       [DATE] NOT NULL
            , [source_name]     [VARCHAR](100) COLLATE Latin1_General_CS_AS    NOT NULL
            , [complete] [BIT] NOT NULL
        ) ON [PRIMARY]
        WITH (DATA_COMPRESSION = PAGE)
    END
