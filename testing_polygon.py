from kvs import KeyValueStorage

kvs = KeyValueStorage('kvs_31', "1234")
# kvs.create_pair('My_pic_4', "/Users/arsenii/Desktop/dsk/pyCourse/kvstask/kvs/140.jpg")
# kvs.create_pair('my_pic_1', "/Users/arsenii/Desktop/dsk/pyCourse/kvstask/kvs/140.jpg")
# print(*kvs.get_item('my_pic_4', ignore_case=True), sep='\n')
# kvs.delete_pair('my_pic_1')
print(kvs.get_commit_log())
# print(kvs.get_item('my_pic_1'))
# print(kvs.list_all_keys())
# print(kvs.search_by_prefix('my'))

# kvs.delete_pair('my_pic_1')

# query_builder = QueryBuilder()
# database = DBHandler('postgres', 'k4v5s6', '87.239.106.32', '5432', 'postgres')

#
# create_table_query = query_builder.build_create_table_query('kvs_1', ['key', 'value'])
# database.execute_create_table_query(create_table_query)
#
# insert_query = query_builder.build_insert_query('kvs_1', ['key', 'value'], 'my_pic', 'eto value')
# database.execute_insert_query(insert_query)
#
# where_query = query_builder.build_where_query('kvs_1', 'my_pic')
# res = database.execute_where_query(where_query)
#
#
# # Hot key


#
# hot_bucket = BucketHandler(hot_bucket_id, hot_bucket_secret, "hot", "kvs-14")
# hot_bucket.upload_file("/Users/arsenii/Desktop/dsk/pyCourse/kvstask/kvs/140.jpg")
#

#
# cold_bucket = BucketHandler(cold_bucket_id, cold_bucket_secret, "cold", "kvs-14")
# cold_bucket.upload_file("/Users/arsenii/Desktop/dsk/pyCourse/kvstask/kvs/140.jpg")

import sqlite3


