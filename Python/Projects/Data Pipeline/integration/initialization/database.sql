
IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'DataPipeline')
    BEGIN
        CREATE DATABASE [DataPipeline]
    END
