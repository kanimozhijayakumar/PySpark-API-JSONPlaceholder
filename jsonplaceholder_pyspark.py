## 🔹 STEP 1: Install Dependencies (Colab)

```python
!apt-get install openjdk-11-jdk-headless -qq
!pip install pyspark requests
```

---

## 🔹 STEP 2: Create Spark Session

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("PySpark API ETL Project") \
    .getOrCreate()

spark
```

---

## 🔹 STEP 3: Fetch Users API Data

```python
import requests

users_url = "https://jsonplaceholder.typicode.com/users"
users_response = requests.get(users_url)

users_data = users_response.json()
users_data[0]
```

---

## 🔹 STEP 4: Convert JSON → Spark DataFrame (SAFE METHOD)

```python
users_rdd = spark.sparkContext.parallelize(users_data)
df_users = spark.read.json(users_rdd)

df_users.show(5)
```

---

## 🔹 STEP 5: View Schema (Important)

```python
df_users.printSchema()
```

---

## 🔹 STEP 6: Flatten Nested JSON

```python
from pyspark.sql.functions import col

df_users_flat = df_users.select(
    col("id"),
    col("name"),
    col("username"),
    col("email"),
    col("address.city").alias("city"),
    col("address.zipcode").alias("zipcode")
)

df_users_flat.show(5)
```

---

## 🔹 STEP 7: Parallel API Calls using PySpark

### Define API function

```python
def fetch_api(url):
    import requests
    return requests.get(url).json()
```

---

### API URLs

```python
api_urls = [
    "https://jsonplaceholder.typicode.com/posts",
    "https://jsonplaceholder.typicode.com/comments",
    "https://jsonplaceholder.typicode.com/todos"
]
```

---

### Parallel execution

```python
api_rdd = spark.sparkContext.parallelize(api_urls)
api_results = api_rdd.map(fetch_api).collect()
```

---

## 🔹 STEP 8: Convert Parallel Results to DataFrames

```python
df_posts = spark.read.json(
    spark.sparkContext.parallelize(api_results[0])
)

df_comments = spark.read.json(
    spark.sparkContext.parallelize(api_results[1])
)

df_todos = spark.read.json(
    spark.sparkContext.parallelize(api_results[2])
)

df_posts.show(5)
df_comments.show(5)
df_todos.show(5)
```

---

## 🔹 STEP 9: Save Output Data (Colab)

```python
df_users_flat.coalesce(1).write.mode("overwrite").json("/content/output/users")
df_posts.coalesce(1).write.mode("overwrite").json("/content/output/posts")
df_todos.coalesce(1).write.mode("overwrite").json("/content/output/todos")

print("Data saved successfully!")
```

---

## 🔹 STEP 10: Stop Spark Session

```python
spark.stop()
```
