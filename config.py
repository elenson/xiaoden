import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'root')
db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')
# 读取阿里云OSS环境变量
oss_access_key_id = os.environ.get("OSS_ACCESS_KEY_ID", 'your_oss_access_key_id')
oss_access_key_secret = os.environ.get("OSS_ACCESS_KEY_SECRET", 'your_oss_access_key_secret')
oss_endpoint = os.environ.get("OSS_ENDPOINT", 'http://your-endpoint.com')
oss_bucket_name = os.environ.get("OSS_BUCKET_NAME", 'your-bucket-name')
