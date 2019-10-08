from pymongo import MongoClient
import pymongo
# 参数为（host，port）
client = MongoClient("127.0.0.1", 27017)
# mydatabase为数据库名称，coltest为集合名称
collection = client["mydatabase"]["coltest7"]

# 插入数据
res = collection.insert_one({"name": "A", "age": 24})
print(res)

res2 = collection.insert_many([{"name": "A", "age": 27}, {"name": "B", "age": 22},
                               {"name": "C", "age": 23}, {"name": "D", "age": 24}])
print(res2)

# 查看数据
res3 = list(collection.find({}))
print(res3)
'''
[{'_id': ObjectId('5d9cc1d7bdbe1b77b829d46d'), 'name': 'A', 'age': 24}, 
{'_id': ObjectId('5d9cc1d7bdbe1b77b829d46e'), 'name': 'A', 'age': 27}, 
{'_id': ObjectId('5d9cc1d7bdbe1b77b829d46f'), 'name': 'B', 'age': 22}, 
{'_id': ObjectId('5d9cc1d7bdbe1b77b829d470'), 'name': 'C', 'age': 23}, 
{'_id': ObjectId('5d9cc1d7bdbe1b77b829d471'), 'name': 'D', 'age': 24}]
'''

res0 = collection.find({})
res_sorted_list = list(res0.sort("age", pymongo.DESCENDING))
print(res_sorted_list)
'''
[{'_id': ObjectId('5d9cc5ea0949487a6325a5cb'), 'name': 'A', 'age': 27}, 
{'_id': ObjectId('5d9cc5ea0949487a6325a5ca'), 'name': 'A', 'age': 24}, 
{'_id': ObjectId('5d9cc5ea0949487a6325a5ce'), 'name': 'D', 'age': 24}, 
{'_id': ObjectId('5d9cc5ea0949487a6325a5cd'), 'name': 'C', 'age': 23}, 
{'_id': ObjectId('5d9cc5ea0949487a6325a5cc'), 'name': 'B', 'age': 22}]
'''

res00 = collection.find({})
res_paging_list = list(res00.sort("age", pymongo.ASCENDING).limit(2).skip(1))
print(res_paging_list)
'''
[{'_id': ObjectId('5d9cc5ea0949487a6325a5cd'), 'name': 'C', 'age': 23}, 
{'_id': ObjectId('5d9cc5ea0949487a6325a5ca'), 'name': 'A', 'age': 24}]
[{'_id': ObjectId('5d9cc5ea0949487a6325a5ca'), 'name': 'A', 'age': 24},
{'_id': ObjectId('5d9cc5ea0949487a6325a5cb'), 'name': 'A', 'age': 27}]
'''

res4 = list(collection.find({"name": "A"}))
print(res4)
'''
[{'_id': ObjectId('5d9cc1d7bdbe1b77b829d46d'), 'name': 'A', 'age': 24}, 
{'_id': ObjectId('5d9cc1d7bdbe1b77b829d46e'), 'name': 'A', 'age': 27}]
'''

# 更改数据
res5 = collection.update_one({"name": "C"}, {"$set": {"name": "F"}})
print(res5)

res6 = collection.update_many({"name": "A"}, {"$set": {"name": "E"}})
print(res6)

# 再次查看数据（验证更改是否成功）
res7 = list(collection.find({}))
print(res7)
'''
[{'_id': ObjectId('5d9cc1d7bdbe1b77b829d46d'), 'name': 'E', 'age': 24}, 
{'_id': ObjectId('5d9cc1d7bdbe1b77b829d46e'), 'name': 'E', 'age': 27}, 
{'_id': ObjectId('5d9cc1d7bdbe1b77b829d46f'), 'name': 'B', 'age': 22}, 
{'_id': ObjectId('5d9cc1d7bdbe1b77b829d470'), 'name': 'F', 'age': 23}, 
{'_id': ObjectId('5d9cc1d7bdbe1b77b829d471'), 'name': 'D', 'age': 24}]
'''

# 删除数据
res8 = collection.delete_one({"name": "D"})
print(res8)

res9 = collection.delete_many({"name": "E"})
print(res9)

# 再次查看数据（验证删除是否成功)
res10 = list(collection.find({}))
print(res10)
'''
[{'_id': ObjectId('5d9cc36531424708b0c299eb'), 'name': 'B', 'age': 22}, 
{'_id': ObjectId('5d9cc36531424708b0c299ec'), 'name': 'F', 'age': 23}]
'''
