
--- Insert sample records
DECLARE @prefix CHAR(26) = 'vendor_'

DECLARE @countries TABLE (country CHAR(1))
INSERT INTO @countries VALUES ('Australia'), ('Brazil'), ('China')
    , ('Denmark'), ('England')


DECLARE @check_date DATETIME = '2023-10-15', @end_date DATETIME = '2023-10-25'

WHILE @check_date <= @end_date
BEGIN
    DECLARE @var_name VARCHAR(50)

    DECLARE name_cursor CURSOR FOR
        SELECT country FROM @countries

        OPEN name_cursor

        FETCH NEXT FROM name_cursor INTO @var_name

        WHILE @@FETCH_STATUS = 0
        BEGIN
            INSERT INTO {db}.{schema}.{tb} (
                [source_date], [source_name], [to_be_processed]
            )
            VALUES (@check_date, @prefix + @var_name + '.csv', 1)

            FETCH NEXT FROM name_cursor INTO @var_name
        END

        CLOSE name_cursor
    DEALLOCATE name_cursor

SET @check_date = @check_date + 1
END
