
- [Initialization](#initialization)
- [Meta](#meta)
- [Basic](#basic)
- [Formatting](#formatting)
- [Function](#function)


## Initialization
```py
import findspark
findspark.init()

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("{AppName}").getOrCreate()

df = spark.read.csv('{file}', inferSchema=True, header=True)
df.columns
df.printSchema()
df.describe().show()
df.show(5)
```


## Meta
```py
from pyspark.sql.types import StructField, StringType, IntegerType, StructType

data_schema = [StructField("{col1}", IntegerType(), True), StructField("{col2}", StringType(), True)]
final_struc = StructType(fields=data_schema)
df = spark.read.json('{file}.json', schema=final_struc)
```


## Basic
```py
type(df['{col1}'])

df.select(['{col1}', '{col2}']).show(truncate=False)
df.filter('{col1} < 30')
# covert the dataframe to list via `collect()`
result = df.filter( (df['{col1}'] < 30) & ~(df['{col2}'] > 20) ).collect()
result[0].asDict()

# create a new column
df.withColumn('{new}', df['{col1}'] + 2)
df.withColumnRenamed('{column}', '{new_column}')

# grouping
df.groupBy('{column}').mean()
df.groupBy('{column}').count()
df.groupBy('{column}').sum()
df.groupBy('{col1}').agg({'{col2}': 'max'})

# ordering
df.orderBy(df['{column}'].desc())

# use SQL
df.createOrReplaceTempView("{table}")
result = spark.sql("SELECT  * FROM  {table}")
```


## Formatting
```py
from pyspark.sql.functions import format_number, dayofmonth, hour, dayofyear, month, year, weekofyear, date_format

df.select(dayofmonth(df['{date}']))
df.select(hour(df['{date}']))

df.select('{date}', format_number('{column}', 2).alias('{alias}'))
df.select(df.column.cast('IntegerType')).alias('{alias}')
```


## Function
```py
from pyspark.sql.functions import countDistinct, avg, stddev, max, min

df.select(countDistinct('{column}').alias('Distinct'))
df.select(avg('{column}').alias('Average'))
df.select(stddev('{column}').alias('StdDev'))

# drop rows with null value in the column
df.na.drop(subset=['{column}'])
# drop rows with any null value
df.na.drop(how='any')
# drop rows only if all value is null
df.na.drop(how='all')

# fill all null value in nominal columns
df.na.fill('new value', subset=['{col1}', '{col3}'])
# fill all null value in numeric columns
df.na.fill(0, subset=['{col2}'])
```
