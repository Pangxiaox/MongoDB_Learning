# MongoDB学习笔记

### 1.关于NoSQL

NoSQL，指的是非关系型的数据库。NoSQL有时也称作Not Only SQL的缩写，是对不同于传统的关系型数据库的数据库管理系统的统称。

NoSQL用于超大规模数据的存储。（例如谷歌或Facebook每天为他们的用户收集万亿比特的数据）。这些类型的数据存储不需要固定的模式，无需多余操作就可以横向扩展。

⭐优缺点分析

优点：

- 高可扩展性
- 数据模型更加灵活，支持键 - 值对存储，列存储，文档存储，图形数据库
- 分布式计算
- 成本较低

缺点：

- 有限的查询功能
- 大多数NoSQL不支持事务机制（MongoDB不支持）
- NoSQL只能保证数据相对一致性



### 2.关于MongoDB

MongoDB 是由C++语言编写的，是一个基于分布式文件存储的开源数据库系统。在高负载的情况下，添加更多的节点，可以保证服务器性能。MongoDB 旨在为WEB应用提供可扩展的高性能数据存储解决方案。MongoDB 将数据存储为一个文档，数据结构由键值(key=>value)对组成。MongoDB 文档类似于 JSON 对象。字段值可以包含其他文档，数组及文档数组。



### 3.MongoDB重点概念

- 数据库

  数据库存储的是文档的集合

  在Mongo shell中可以通过use命令连接到需要用到的数据库

  ```
  > use MyNewDB
  switched to db MyNewDB
  ```

  在Mongo shell中可以通过db命令展示当前数据库对象或者叫集合

  ```shell
  > db
  MyNewDB
  ```

  在Mongo shell中可以通过show dbs命令显示所有数据的列表

  ```shell
  > show dbs
  MyNewDB 0.000GB
  admin 0.000GB
  config 0.000GB
  local 0.000GB
  test 0.000GB
  ```

  ▲想要展示出MyNewDB，需要先往那个数据库插入一些数据，执行完前面两项命令之后马上show dbs是不会显示MyNewDB出来的。

- 集合

  集合就是 MongoDB 文档组，类似于 RDBMS （关系数据库管理系统：Relational Database Management System)中的表格。集合存在于数据库中，集合没有固定的结构，这意味着你在对集合可以插入不同格式和类型的数据，但通常情况下我们插入集合的数据都会有一定的关联性。

- 文档

  文档是一组键值(key-value)对(即 BSON)。文档的数据结构和 JSON 基本一样。所有存储在集合中的数据都是 BSON 格式。BSON 是一种类似 JSON 的二进制形式的存储格式，是 Binary JSON 的简称。MongoDB 的文档不需要设置相同的字段，并且相同的字段不需要相同的数据类型，这与关系型数据库有很大的区别，也是 MongoDB 非常突出的特点。



### 4.MongoDB数据库操作

##### 4.1 创建数据库

```shell
use DATABASE_NAME
```

▲如果数据库不存在则创建该数据库，否则切换到指定数据库

```shell
> use MyDB
switched to db MyDB
> db
MyDB
```

##### 4.2 删除数据库

```shell
db.dropDatabase()
```

▲删除当前数据库，默认为test，可以通过db命令查看当前的数据库名

```shell
> use MyDB
switched to db MyDB
> db
MyDB
> db.dropDatabase()
{ "dropped" : "MyDB", "ok" : 1 }
```



### 5.MongoDB集合操作

##### 5.1 创建集合

```shell
db.createCollection(name,options)
```

▲name：要创建的集合名

​	options：可选参数

options：

| 字段        | 类型 | 描述                                                         |
| ----------- | ---- | ------------------------------------------------------------ |
| capped      | 布尔 | （可选）如果为 true，则创建固定集合。固定集合是指有着固定大小的集合，当达到最大值时，它会自动覆盖最早的文档。当该值为 true 时，必须指定 size 参数。 |
| autoIndexId | 布尔 | （可选）如为 true，自动在 _id 字段创建索引。默认为 false。   |
| size        | 数值 | （可选）为固定集合指定一个最大值，以千字节计（KB）。如果 capped 为 true，也需要指定该字段。 |
| max         | 数值 | （可选）指定固定集合中包含文档的最大数量。                   |

▲在插入文档时，MongoDB 首先检查固定集合的 size 字段，然后检查 max 字段。

```shell
> use newDB
switched to db newDB
> db.createCollection("test0")
{"ok":1}
> show tables
test0
> show collections
test0
> db.createCollection("test1",{capped:true,autoIndexId:true,size:6142800,max:10000})
{
"note":"the autoIndexId option is deprecated and will be removed in a future release",
"ok":1
}
```

▲用show tables命令或show collections命令来查看已有集合

▲上面带参数的表示创建固定集合test1，整个集合空间大小6142800KB，文档最大个数为10000个

⭐实际上，在MongoDB中，不需要显式创建集合，当插入一些文档时，MongoDB会自动创建集合，如下：

```shell
> db.test2.insert({x:2})
WriteResult({"nInserted":1})
> show tables
test2
```

##### 5.2 删除集合

```shell
db.collection.drop()
```

▲如果成功删除选定的集合，`drop()`方法返回true，否则返回false

```shell
...
> db.a.drop()
true
> show tables
> db.a.drop()
false
```



### 6.MongoDB文档操作

##### 6.1 插入文档

```shell
db.COLLECTION_NAME.insert(document)
```

▲MongoDB中可使用如上的 `insert()`方法或 `save()`方法向集合中插入文档

```shell
> db.b.insert({x:1,y:[1,2],z:"1"})
WriteResult({"nInserted":1})
> db.b.find()
{"_id":ObjectId("5d90d4ab9f849cdcf7dd4df6"),"x":1,"y":[1,2],"z":"1"}
> doc = ({x:1})
{"x":1}
> db.b.save(doc)
WriteResult({"nInserted":1})
```

▲上面所示 `find()`方法可以查看已经插入的文档。如果不指定 _id 字段 save() 方法类似于 insert() 方法。如果指定 _id 字段，则会更新该 _id 的数据。另外，我们也可以把数据定义为一个变量（如上例的doc），然后再执行插入操作。

```shell
> db.c.insertOne({x:1})
{
	"acknowledged":true,
	"insertedId":ObjectId("5d90d8df9f849cdcf7dd4df8")
}

> db.d.insertMany([{x:1},{y:2}])
{
	"acknowledged":true,
	"insertedIds":[
			ObjectId("5d90db1e9f849cdcf7dd4df9"),
			ObjectId("5d90db1e9f849cdcf7dd4dfa")
	]
}
```

▲Ver 3.2之后还有如上例的两种方法插入文档，即

- db.collection.insertOne()：向指定集合中插入一条文档数据
- db.collection.insertMany()：向指定集合中插入多条文档数据

```shell
> var arr = []; for(var i=1;i<5;i++){
... arr.push({x:i})
... }
4
> db.num.insert(arr)
BulkWriteResult({
	"writeErrors":[ ],
	"writeConcernErrors":[ ],
	"nInserted":4,
	"nUpsertd":0,
	"nMatched":0,
	"nModified":0,
	"nRemoved":0,
	"upserted":[ ]
})
```

▲一次性插入多条数据的另一种方法（通过数组实现）

##### 6.2 更新文档

`update()`方法

```shell
db.collection.update(
   <query>,
   <update>,
   {
     upsert: <boolean>,
     multi: <boolean>,
     writeConcern: <document>
   }
)
```

▲参数说明：

​	query：update的查询条件，类似sql update查询内where后面的。

​	update：update的对象和一些更新的操作符（如$,$inc...）等，也可以理解为sql update查询内set后面的。

​	upsert：可选，如果不存在update的记录，是否插入objNew,true为插入，默认是false，不插入。

​	multi：可选，mongodb 默认是false,只更新找到的第一条记录，如果这个参数为true,就把按条件查出来多条记录全部更新。

​	writeConcern：可选，抛出异常的级别。

```shell
> db.a.insert({x:1,y:2})
WriteResult({"nInserted":1})
> db.a.find()
{"_id":ObjectId("5d916288c6d49f0e76db68a9"),"x":1,"y":2}
> db.a.update({y:2},{$set:{y:1}})
WriteResult({"nMatched":1,"nUpserted":0,"nModified":1})
> db.a.find()
{"_id":ObjectId("5d916288c6d49f0e76db68a9"),"x":1,"y":1}
> db.b.insert({x:1,y:1})
WriteResult({"nInserted":1})
> db.b.insert({x:1,y:2})
WriteResult({"nInserted":1})
> db.b.update({x:1},{$set:{x:2}},{multi:true})
WriteResult({"nMatched":2,"nUpserted":0,"nModified":2})
> db.b.find()
{"_id":ObjectId("5d916cb7c6d49f0e76db68ab"),"x":2,"y":1}
{"_id":ObjectId("5d916cb3c6d49f0e76db68ac"),"x":2,"y":1}
```

`save()`方法

```shell
db.collection.save(
   <document>,
   {
     writeConcern: <document>
   }
)
```

▲参数说明：

document：文档数据

writeConcern：可选，抛出异常的级别

```shell
> db.c.insert({x:1})
WriteResult({"nInserted":1})
> db.c.find()
{"_id":ObjectId("5d91746cc6d49f0e76db68ad"),"x":1}
> db.c.save({"_id":ObjectId("5d91746cc6d49f0e76db68ad"),x:4})
WriteResult({"nMatched":1,"nUpserted":0,"nModified":1})
> db.c.find()
{"_id":ObjectId("5d91746cc6d49f0e76db68ad"),"x":4}
```

▲Ver 3.2之后还有如下例的两种方式更新集合文档

- db.collection.updateOne()：向指定集合更新单个文档
- db.collection.updateMany()：向指定集合更新多个文档

```shell
> db.d.insert({x:1})
WriteResult({"nInserted":1})
> db.d.updateOne({x:1},{$set:{x:2}})
{"acknowledeged":true,"matchedCount":1,"modifiedCount":1}
> db.d.find()
{"_id":ObjectId("5d917a77c6d49f0e76db68af"),"x":2}
> db.e.insert({x:1})
WriteResult({"nInserted":1})
> db.e.insert({x:2})
WriteResult({"nInserted":1})

> db.e.updateMany({x:{$lt:5}},{$set:{x:3}})
{"acknowledged":true,"matchedCount":2,"modifiedCount":2}
> db.e.find()
{"_id":ObjectId("5d917c16c6d49f0e76db68b0"),"x":3}
{"_id":ObjectId("5d917c1ec6d49f0e76db68b1"),"x":3}
```

▲writeConcern参数：

- WriteConcern.NONE：没有异常抛出
- WriteConcern.NORMAL：仅抛出网络错误异常，没有服务器错误异常
- WriteConcern.SAFE：抛出网络错误异常、服务器错误异常；并等待服务器完成写操作
- WriteConcern.MAJORITY：抛出网络错误异常、服务器错误异常；并等待一个主服务器完成写操作
- WriteConcern.FSYNC_SAFE：抛出网络错误异常、服务器错误异常；写操作等待服务器将数据刷新到磁盘
- WriteConcern.JOURNAL_SAFE：抛出网络错误异常、服务器错误异常；写操作等待服务器提交到磁盘的日志文件
- WriteConcern.REPLICAS_SAFE：抛出网络错误异常、服务器错误异常；等待至少2台服务器完成写操作

##### 6.3 删除文档

```shell
db.collection.remove(
   <query>,
   <justOne>
)
```

Ver 2.6之后改为：

```shell
db.collection.remove(
   <query>,
   {
     justOne: <boolean>,
     writeConcern: <document>
   }
)
```

▲参数说明：

​	query：（可选）删除的文档的条件

​	justOne：（可选）如果设置为true或1，则只删除一个文档，如果不设置该参数，或使用默认值false，则删除所有匹配条件的文档

​	writeConcern：（可选）抛出异常的级别

```shell
> use testing
> db
testing
> db.a.insert({x:1})
> db.a.insert({x:1})
> db.a.insert({x:2})
> db.a.remove({x:1},1)				#删除一个
WriteResult({"nRemoved":1})
> db.a.find()
{"_id":ObjectId("5d930c9a20ec6d9af063ce95"),"x":1}
{"_id":ObjectId("5d930ca120ec6d9af063ce96"),"x":2}
> db.a.remove({}) 					#全部删除
WriteResult({"nRemoved":2})
> db.a.find()
> db.a.insert({x:1})
> db.a.insert({x:1})
> db.a.insert({x:1})
> db.a.remove({x:1})
WriteResult({"nRemoved":3})
```

▲现在推荐使用如下例方法删除文档：

- db.collection.deleteOne()：删除指定集合的一个文档
- db.collection.deleteMany()：删除指定集合的多个文档

```shell
> db
test
> db.b.insert({x:1})
> db.b.insert({x:1})
> db.b.insert({x:2})
> db.b.deleteMany({x:1})
{"acknowledged":true,"deletedCount":2}
> db.b.find()
{"_id":ObjectId("5d93113caf133f7c0ef3ec10","x":2)}
> db.b.insert({x:2})
> db.b.find()
{"_id":ObjectId("5d93113caf133f7c0ef3ec10"),"x":2}
{"_id":ObjectId("5d9311dcaf133f7c0ef3ec11"),"x":2}
> db.b.deleteOne({x:2})
{"acknowledged":true,"deletedCount":1}
> db.b.find()
{"_id":ObjectId("5d9311dcaf133f7c0ef3ec11"),"x":2}
> db.b.deleteMany({})			#删除全部
{"acknowledged":true,"deletedCount":1}
> db.b.find()			#没有数据
```



##### 6.4 查询文档

```shell
db.collection.find(query, projection)`
```

▲ `find()`方法以非结构化的方式显示所有文档

​	参数说明：

​	query：可选，使用查询操作符指定查询条件

​	projection：可选，使用投影操作符指定返回的键。如想查询时返回文档中所有键值，只需省略该参数即可（默认省略）

```shell
db.col.find().pretty()
```

▲如果想要以易读的方式来读取数据，可使用如上的 `pretty()`方法， `pretty()`方法以格式化的方式显示所有文档。

```shell
> use database
> db.a.insert({x:1})
> db.a.insert({x:1})
> db.a.find()
{"_id":ObjectId("5d954f563ae1f136110b35ef"),"x":1}
{"_id":ObjectId("5d954f5b3ae1f136110b35f0"),"x":1}
> db.a.findOne()
{"_id":ObjectId("5d954f563ae1f136110b35ef"),"x":1}
```

▲此外，还可以使用如上的 `findOne()`方法查询文档，它只返回一个文档。

⭐MongoDB与RDBMS where语句比较

| 操作       | 格式                   | MongoDB范例                 | RDBMS中类似语句 |
| ---------- | ---------------------- | --------------------------- | --------------- |
| 等于       | {<key>:<value>}        | db.col.find({"x":1})        | where x=1       |
| 小于       | {<key>:{$lt:<value>}}  | db.col.find({"x":{$lt:1}})  | where x<1       |
| 小于或等于 | {<key>:{$lte:<value>}} | db.col.find({"x":{$lte:1}}) | where x<=1      |
| 大于       | {<key>:{$gt:<value>}}  | db.col.find({"x":{$gt:1}})  | where x>1       |
| 大于或等于 | {<key>:{$gte:<value>}} | db.col.find({"x":{$gte:1}}) | where x>=1      |
| 不等于     | {<key>:{$ne:<value>}}  | db.col.find({"x":{$ne:1}})  | where x!=1      |

⭐MongoDB and条件

```shell
db.col.find({key1:value1, key2:value2}).pretty()
```

▲MongoDB 的 find() 方法可以传入多个键(key)，每个键(key)以逗号隔开，即常规 SQL  的 AND 条件。

```shell
> db.b.insert({x:1,y:1})
> db.b.insert({x:1,y:2})
> db.b.find({x:1,y:1})
{"_id":ObjectId("5d9557543ae1f136110b35f1"),"x":1,"y":1}
```

如上示例，相当于where语句： where x=1 and y=1

⭐MongoDB or条件

```shell
db.col.find(
   {
      $or: [
         {key1: value1}, {key2:value2}
      ]
   }
).pretty()
```

```shell
> db.b.insert({x:1,y:1})
> db.b.insert({x:1,y:2})
> db.b.find({$or:[{x:1},{y:2}]})
{"_id":ObjectId("5d9557543ae1f136110b35f1"),"x":1,"y":1}
{"_id":ObjectId("5d95575e3ae1f136110b35f2"),"x":1,"y":2}
```

如上示例，相当于where语句：where x=1 or y=2

⭐and 与 or 联合使用

```shell
> db.b.insert({x:1,y:1})
> db.b.insert({x:1,y:2})
> db.b.find({y:2,$or:[{x:1},{x:2}]})
{"_id":ObjectId("5d95575e3ae1f136110b35f2"),"x":1,"y":2}
```

如上示例，相当于where语句：where y=2 and (x=1 or x=2)

⭐参数projection用法

若不指定projection,则默认返回所有键，指定projection格式如下：

```shell
> db.c.insert({x:1,y:2,z:3})
> db.c.insert({x:4,y:5,z:6})
> db.c.insert({x:7,y:8,z:9})
> db.c.find({x:7},{y:1}) 	// inclusion模式 指定返回的键，不返回其他键
{"_id":ObjectId("5d9565833ae1f136110b35f5"),"y":8}
> db.c.find({x:7},{y:0}) 	// exclusion模式 指定不返回的键,返回其他键
{"_id":ObjectId("5d9565833ae1f136110b35f5"),"x":7,"z":9}
> db.c.find({x:7},{_id:0,y:1})  	// _id 键默认返回，需要主动指定 _id:0 才会隐藏
{"y":8}
> db.c.find({x:7},{y:1,z:0})  	// 错误 两种模式不可混用！！！！
Error:error:{
	"ok":0,
	"errmsg":"Projection cannot have a mix of inclusion and exclusion."
	"code":2,
	"codeName":"BadValue"
}
> db.c.find({x:7},{_id:0,x:0,z:0})  // exclusion模式 指定不返回的键,返回其他键
{"y":8}
> db.c.find({x:7},{_id:0,x:1,z:1})  // inclusion模式 指定返回的键，不返回其他键
{"x":7,"z":9}
```



### 7.MongoDB 条件操作符

- $gt：大于
- $gte：大于或等于
- $lt：小于
- $lte：小于或等于
- $eq：等于
- $ne：不等于

```shell
> use db
> db.a.insert({x:1})
> db.a.insert({x:2})
> db.a.insert({x:3})
> db.a.insert({x:4})
> db.a.find({x:{$gt:2}},{_id:0})
{"x":3}
{"x":4}
> db.a.find({x:{$gte:3}},{_id:0})
{"x":3}
{"x":4}
> db.a.find({x:{$lt:2}},{_id:0})
{"x":1}
> db.a.find({x:{$lte:1}},{_id:0})
{"x":1}
> db.a.find({x:{$eq:2}},{_id:0})
{"x":2}
> db.a.find({x:{$ne:4,$lt:2}},{_id:0})
{"x":1}
```



### 8.MongoDB $type操作符

$type操作符是基于BSON类型来检索集合中匹配的数据类型，并返回结果。

MongoDB中可以使用的类型（常用，节选）如下表示：

| 类型           | 数字 | Alias    |
| -------------- | ---- | -------- |
| Double         | 1    | “double” |
| String         | 2    | "string" |
| Boolean        | 8    | "bool"   |
| Date           | 9    | "date"   |
| Null           | 10   | "null"   |
| 32-bit integer | 16   | "int"    |
| 64-bit integer | 18   | "long"   |

```shell
> db.a.insert({x:"12"})
> db.a.insert({x:12})
> db.a.insert({x:true})
> db.a.insert({x:null})
> db.a.insert({x:0.5})
> db.a.find({x:{$type:1}},{_id:0})
{"x":12}
{"x":0.5}
> db.a.find({x:{$type:2}},{_id:0})
{"x":"12"}
> db.a.find({x:{$type:8}},{_id:0})
{"x":true}
> db.a.find({x:{$type:10}},{_id:0})
{"x":null}
> db.a.find({x:{$type:'string'}},{_id:0})  //第二种方式，string为alias
{"x":"12"}
> db.a.find({x:{$type:'bool'}},{_id:0})  //第二种方式，bool为alias
{"x":true}
```



### 9.MongoDB limit()和skip()方法

`limit()`方法

```shell
db.COLLECTION_NAME.find().limit(NUMBER)
```

▲用于在MongoDB中读取指定数量的数据记录，参数NUMBER指定从MongoDB中读取的记录条数

```shell
> db.a.insert({x:1})
> db.a.insert({x:2})
> db.a.insert({x:3})
> db.a.insert({x:4})
> db.collect.find({},{_id:0}).limit(2)
{"x":1}
{"x":2}
```

`skip()`方法

```shell
db.COLLECTION_NAME.find().limit(NUMBER).skip(NUMBER)
```

▲使用skip()方法来跳过指定数量的数据，skip方法同样接受一个NUMBER参数作为跳过的记录条数。 `skip()`方法默认参数为0.

```shell
> db.a.insert({x:1})
> db.a.insert({x:2})
> db.a.insert({x:3})
> db.a.insert({x:4})
> db.a.find({},{_id:0}).limit(2).skip(1)
{"x":2}
{"x":3}
```

⭐ `skip()`方法和 `limit()`方法结合可以实现分页，但只适合于小数据量分页，如果是百万级效率就会非常低，因为skip方法是一条条数据数过去的。



### 10.MongoDB 排序

```shell
db.COLLECTION_NAME.find().sort({KEY:1/-1})
```

▲使用 `sort()`方法对数据进行排序，sort方法通过KEY参数指定排序的字段，并使用1或者-1来指定排序方式，其中1表示升序排列，-1表示降序排列。

```shell
> db.a.insert({x:2})
> db.a.insert({x:3})
> db.a.insert({x:1})
> db.a.insert({x:4})
> db.a.find({},{_id:0}).sort({x:1}) 
{"x":1}
{"x":2}
{"x":3}
{"x":4}
> db.a.find({},{_id:0}).sort({x:-1})
{"x":4}
{"x":3}
{"x":2}
{"x":1}
```

⭐ `skip()`，`limit()`，`sort()`三个方法放在一起用时，执行顺序是先 `sort()`，然后 `skip()`，最后 `limit()`。



### 11.MongoDB 索引

索引通常能够极大的提高查询的效率，如果没有索引，MongoDB在读取数据时必须扫描集合中的每个文件并选取那些符合查询条件的记录。 这种扫描全集合的查询效率是非常低的，特别在处理大量的数据时，查询可以要花费几十秒甚至几分钟，这对网站的性能是非常致命的。 索引是特殊的数据结构，索引存储在一个易于遍历读取的数据集合中，索引是对数据库表中一列或多列的值进行排序的一种结构 。

`createIndex()`方法

```shell
db.collection.createIndex({keys:1/-1}, options)
```

▲Ver 3.0之前创建索引方法是db.collection.ensureIndex().

​	参数keys为你要创建的索引字段，1表示指定按升序创建索引，-1表示指定按降序创建索引

```shell
> db.col.createIndex({x:1})
```

▲也可以设置使用多个字段创建索引（类似于关系型数据库中的复合索引）

```shell
> db.col.createIndex({x:1,y:-1})
```

​	参数options可选列表如下：

| Parameter          | Type          | Description                                                  |
| ------------------ | ------------- | ------------------------------------------------------------ |
| background         | Boolean       | 建索引过程会阻塞其它数据库操作，background可指定以后台方式创建索引，即增加 "background" 可选参数。"background" 默认值为**false**。 |
| unique             | Boolean       | 建立的索引是否唯一。指定为true创建唯一索引。默认值为**false**。 |
| name               | String        | 索引的名称。如果未指定，MongoDB的通过连接索引的字段名和排序顺序生成一个索引名称。 |
| dropDups           | Boolean       | **3.0+版本已废弃。**在建立唯一索引时是否删除重复记录,指定 true 创建唯一索引。默认值为 **false**。 |
| sparse             | Boolean       | 对文档中不存在的字段数据不启用索引；这个参数需要特别注意，如果设置为true的话，在索引字段中不会查询出不包含对应字段的文档.。默认值为 **false**。 |
| expireAfterSeconds | integer       | 指定一个以秒为单位的数值，完成 TTL设定，设定集合的生存时间。 |
| v                  | index version | 索引的版本号。默认的索引版本取决于mongod创建索引时运行的版本。 |
| weights            | document      | 索引权重值，数值在 1 到 99,999 之间，表示该索引相对于其他索引字段的得分权重。 |
| default_language   | string        | 对于文本索引，该参数决定了停用词及词干和词器的规则的列表。 默认为英语。 |
| language_override  | string        | 对于文本索引，该参数指定了包含在文档中的字段名，语言覆盖默认的language，默认值为 language。 |

如下例子：在后台创建索引

```shell
db.a.createIndex({x: 1, y: 1}, {background: true})
```

▲其他有用的方法：

- 查看集合索引

```shell
db.col.getIndexes()
```

- 查看集合索引大小

```shell
db.col.totalIndexSize()
```

- 删除集合所有索引

```shell
db.col.dropIndexes()
```

- 删除集合指定索引

```shell
db.col.dropIndex("索引名")
```



### 12.MongoDB 聚合

MongoDB中聚合(aggregate)主要用于处理数据(诸如统计平均值,求和等)，并返回计算后的数据结果。

`aggregate()`方法

```shell
db.COLLECTION_NAME.aggregate(AGGREGATE_OPERATION)
```

```shell
> db.a.insert({x:1,user:"A"})
> db.a.insert({x:4,user:"A"})
> db.a.insert({x:10,user:"A"})
> db.a.insert({x:8,user:"B"})
> db.a.aggregate([{$group:{_id:"$user",num:{$sum:"$x"}}}])
{"_id":"A","num":15}
{"_id":"B","num":8}
> db.a.aggregate([{$group:{_id:"$user",avg:{$avg:"$x"}}}])
{"_id":"A","avg":5}
{"_id":"B","avg":8}
> db.a.aggregate([{$group:{_id:"$user",max:{$max:"$x"}}}])
{"_id":"B","max":8}
{"_id":"A","max":10}
> db.a.aggregate([{$group:{_id:"$user",number:{$sum:1}}}])  //count计数
{"_id":"B","number":1}
{"_id":"A","number":3}
```

下图展示部分常用的聚合表达式：

| 表达式    | 描述                                         | 实例                                                         |
| --------- | -------------------------------------------- | ------------------------------------------------------------ |
| $sum      | 计算总和                                     | db.a.aggregate([{$group : {_id : "$user", num : {$sum : "$x"}}}]) |
| $avg      | 计算平均值                                   | db.a.aggregate([{$group : {_id : "$user", avg : {$avg : "$x"}}}]) |
| $min      | 获取集合中所有文档对应值的最小值             | db.a.aggregate([{$group : {_id : "$user", min : {$min : "$x"}}}]) |
| $max      | 获取集合中所有文档对应值的最大值             | db.a.aggregate([{$group : {_id : "$user", max : {$max : "$x"}}}]) |
| $push     | 在结果文档中插入值到一个数组中               | db.a.aggregate([{$group : {_id : "$user", push : {$push : "$x"}}}]) |
| $addToSet | 在结果文档中插入值到一个数组中，但不创建副本 | db.a.aggregate([{$group : {_id : "$user", addToSet : {$addToSet : "$x"}}}]) |
| $first    | 根据资源文档的排序获取第一个文档数据         | db.a.aggregate([{$group : {_id : "$user", first : {$first : "$x"}}}]) |
| $last     | 根据资源文档的排序获取最后一个文档数据       | db.a.aggregate([{$group : {_id : "$user", last : {$last : "$x"}}}]) |

管道

管道在Unix和Linux中一般用于将当前命令的输出结果作为下一个命令的参数。 

MongoDB的聚合管道将MongoDB文档在一个管道处理完毕后将结果传递给下一个管道处理。管道操作是可以重复的。

表达式：处理输入文档并输出。表达式是无状态的，只能用于计算当前聚合管道的文档，不能处理其它的文档。

▲聚合框架中几个常用操作：

- $project：修改输入文档的结构。可以用来重命名、增加或删除域，也可以用于创建计算结果以及嵌套文档。

- $match：用于过滤数据，只输出符合条件的文档。$match使用MongoDB的标准查询操作。

- $limit：限制MongoDB聚合管道返回的文档数。

- $skip：在聚合管道中跳过指定数量的文档，并返回余下的文档。

- $unwind：将文档中的某一个数组类型字段拆分成多条，每条包含数组中的一个值。

- $group：将集合中的文档分组，用于统计结果。

- $sort：将输入文档排序后输出。

- $geoNear：输出接近某一地理位置的有序文档

  1. $project示例

     ```shell
     db.article.aggregate(
         { $project : {
             title : 1 ,
             author : 1 ,
         }}
      );
     ```

     这样，结果中只有_id,title,author三个字段，默认 _id字段是被包含的，如果想要不包含 _id字段，可以如下操作：

     ```shell
     db.article.aggregate(
         { $project : {
             _id : 0 ,
             title : 1 ,
             author : 1
         }});
     ```

  2. $match示例

     ```shell
     db.articles.aggregate( [
                             { $match : { score : { $gt : 70, $lte : 90 } } },
                             { $group: { _id: null, count: { $sum: 1 } } }
                            ] );
     ```

     $match用于获取分数大于70以及小于等于90的记录，然后将符合条件的记录送到下一阶段$group管道操作符进行处理。

  3. $skip示例

     ```shell
     db.article.aggregate(
         { $skip : 3 });
     ```

     经过$skip管道操作符处理后，前3个文档被"过滤"掉。



### 13.MongoDB ObjectId

ObjectId是一个12字节BSON类型数据，格式如下：

- 前4个字节表示时间戳
- 接下来3个字节是机器识别码
- 紧接着的2个字节由进程id组成（PID）
- 最后3个字节是随机数

MongoDB中存储的文档必须有一个"_id"键。这个键的值可以是任何类型，默认是一个ObjectId对象。在一个集合里，每个文档都有唯一的" _id"值，来确保集合里每个文档都能被唯一标识。MongoDB采用ObjectId而不是其他比较常规做法（如自动增加的主键）的主要原因是：在多个服务器上同步自动增加主键值费力费时。

##### 13.1 创建新的ObjectId

```shell
> newId = ObjectId()
ObjectId("5d99e38a1fbb2ecf41145ab8")
// 返回以上唯一生成的id
> myId = ObjectId("5d99e38a1fbb2ecf41145ab9") 
//用生成的id取代MongoDB自动生成的ObjectId
```

##### 13.2 创建文档的时间戳

由于ObjectId存储了4个字节的时间戳，可以通过 getTimestamp  函数来获取文档的创建时间。

```shell
> ObjectId("5d99e4be1fbb2ecf41145ab9").getTimestamp()
ISODate("2019-10-06T12:57:34Z")
```

##### 13.3 ObjectId转换为字符串

```shell
> new ObjectId().str
5d99e7011fbb2ecf41145aba
```



### 14.MongoDB 关系

MongoDB的关系表示多个文档之间在逻辑上的相互联系，文档之间可以通过嵌入和引用来建立联系。

MongoDB中关系可以是：1：1（一对一）、1：N（一对多）、N：1（多对一）、N：N（多对多）

考虑user和car的关系，一个用户可以拥有多辆车，即一对多关系。

以下是user文档的简单结构：

```shell
{
	"_id":ObjectId("5d99e87f1fbb2ecf41145abb"),
	"name":"Ann",
	"phone":"1425"
}
```

以下是car文档的简单结构：

```shell
{
	"_id":ObjectId("5d99e9551fbb2ecf41145abc"),
	"color":"black",
	"size":"medium"
}
{
	"_id":ObjectId("5d99e96a1fbb2ecf41145abd"),
	"color":"red",
	"size":"small"
}
```

##### 14.1 嵌入式关系

```shell
{
	"_id":ObjectId("5d99eaaf1fbb2ecf41145abe"),
	"name":"Ann",
	"phone":"1425",
	"car":[
		{
			"color":"black",
			"size":"medium"
		},
		{
			"color":"red",
			"size":"small"
		}
	]
}
```

以上数据保存在单一文档中，比较容易获取和维护数据，可以这样来查询用户所拥有的车辆：

```shell
> db.users.findOne({"name":"Ann"},{"car":1})
{
	"_id":ObjectId("5d99eaaf1fbb2ecf41145abe"),
	"car":[
		{
			"color":"black",
			"size":"medium"
		},
		{
			"color":"red",
			"size":"small"
		}
	]
}
```

▲缺点：如果用户（user)和车辆(car)在不断增加，数据量不断变大，影响读写性能。

##### 14.2 引用式关系

引用式关系是设计数据库时经常用到的方法，这种方法把用户数据文档和用户地址数据文档分开，通过引用文档的 **id** 字段来建立关系。

```shell
{
	"_id":ObjectId("5d99eddd1fbb2ecf41145abf"),
	"name":"Ann",
	"phone":"1425",
	"car_ids":[
		ObjectId("5d99e9551fbb2ecf41145abc"),
		ObjectId("5d99e96a1fbb2ecf41145abd")
	]
}
```

以上示例中，用户文档的car_ids字段包含用户拥有车辆的对象id（ObjectId）数组。

我们可以读取这些ObjectId来获取用户的详细车辆信息。

如下示例，需要用到两次查询操作，第一次查询用户拥有车辆的ObjectId，第二次通过获取到的ObjectId查询更加详细的用户车辆信息。

```shell
> var result = db.users_s.findOne({"name":"Ann"},{"car_ids":1})
> result
{
	"_id":ObjectId("5d99eddd1fbb2ecf41145abf"),
	"car_ids":[
		ObjectId("5d99e9551fbb2ecf41145abc"),
		ObjectId("5d99e96a1fbb2ecf41145abd")
	]
}
> var cars = db.car.find({"_id":{"$in":result["car_ids"]}})
> cars
{"_id":ObjectId("5d99e9551fbb2ecf41145abc"),"color":"black","size":"medium"}
{"_id":ObjectId("5d99e96a1fbb2ecf41145abd"),"color":"red","size":"small"}
```



### 15.MongoDB 数据库引用

MongoDB引用有两种：

- 手动引用（Manual References)
- DBRefs

使用手动引用：

**参看上面第14点的引用式关系**

使用DBRefs：

```shell
{ $ref : , $id : , $db :  }
```

▲三个字段的意义：

​	$ref：集合名称

​	$id：引用的id

​	$db：数据库名称，可选参数

```shell
> db.a.insert({x:1,y:2,z:3})
> db.b.insert({x:4,y:5,z:6})
> db.c.insert({x:7,y:8,z:9})
> db.user.insert({"name":"Ann","res":{"$ref":"b","$id":ObjectId("5d9a9f6bdc0ca3f907c04842")}})
> var user = db.user.findOne({"name":"Ann"})
> var dbRef = user.res
> db[dbRef.$ref].findOne({"_id":(dbRef.$id)})
{"_id":ObjectId("5d9a9f6bdc0ca3f907c04842"),"x":4,"y":5,"z":6}
```



### 16.MongoDB 覆盖索引查询

覆盖查询是指：

- 所有的查询字段是索引的一部分
- 所有的查询返回字段在同一个索引中

这种情况，MongoDB无需在整个数据文档中检索匹配查询条件，从索引中获取数据要快得多

```shell
> db.a.insert({x:1,y:2,z:3})
> db.a.createIndex({x:1,y:1})
{
	"createdCollectionAutomatically":false,
	"numIndexesBefore":1,
	"numIndexedAfter":2,
	"ok":1
}
> db.a.find({x:1},{y:1,_id:0})    //查询1
{"y":2}
> db.a.find({x:1},{y:1})     //查询2
{"_id":ObjectId("5d9a9f4ddc0ca3f907c048f1"),"y":2}
```

▲先在a集合创建联合索引，该索引会覆盖查询1，但不会覆盖查询2.（因为查询2没有排除 _id）

不能使用覆盖索引查询的情况：

- 所有索引字段是一个数组
- 所有索引字段是一个子文档



### 17.MongoDB 查询分析

MongoDB 查询分析可以确保我们所建立的索引是否有效，是查询语句性能分析的重要工具。

##### 17.1 使用explain()

```shell
> db.b.insert({x:4,y:5,z:6})
> db.b.ensureIndex({x:1,y:1})
> db.b.find({x:4},{y:1,_id:0}).explain()
{
        "queryPlanner" : {
                "plannerVersion" : 1,
                "namespace" : "testref.b",
                "indexFilterSet" : false,
                "parsedQuery" : {
                        "x" : {
                                "$eq" : 4
                        }
                },
                "queryHash" : "2AAAA4A9",
                "planCacheKey" : "8B78F5A0",
                "winningPlan" : {
                        "stage" : "PROJECTION_COVERED",
                        "transformBy" : {
                                "y" : 1,
                                "_id" : 0
                        },
                        "inputStage" : {
                                "stage" : "IXSCAN",
                                "keyPattern" : {
                                        "x" : 1,
                                        "y" : 1
                                },
                                "indexName" : "x_1_y_1",
                                "isMultiKey" : false,
                                "multiKeyPaths" : {
                                        "x" : [ ],
                                        "y" : [ ]
                                },
                                "isUnique" : false,
                                "isSparse" : false,
                                "isPartial" : false,
                                "indexVersion" : 2,
                                "direction" : "forward",
                                "indexBounds" : {
                                        "x" : [
                                                "[4.0, 4.0]"
                                        ],
                                        "y" : [
                                                "[MinKey, MaxKey]"
                                        ]
                                }
                        }
                },
                "rejectedPlans" : [ ]
        },
        "serverInfo" : {
                "host" : "<//HOSTNAME_HERE//>",
                "port" : 27017,
                "version" : "4.2.0",
                "gitVersion" : "a4b751dcf51dd249c5865812b390cfd1c0129c30"
        },
        "ok" : 1
}
```

##### 17.2 使用hint()

虽然MongoDB查询优化器一般工作的很不错，但是也可以使用 hint 来强制 MongoDB 使用一个指定的索引。

```shell
> db.b.insert({x:4,y:5,z:6})
> db.b.ensureIndex({x:1,y:1})
> db.b.find({x:4},{y:1,_id:0}).hint({x:1,y:1})
{"y":5}
> db.b.find({x:4},{y:1,_id:0}).hint({x:1,y:1}).explain()
{
        "queryPlanner" : {
                "plannerVersion" : 1,
                "namespace" : "testref.b",
                "indexFilterSet" : false,
                "parsedQuery" : {
                        "x" : {
                                "$eq" : 4
                        }
                },
                "queryHash" : "2AAAA4A9",
                "planCacheKey" : "8B78F5A0",
                "winningPlan" : {
                        "stage" : "PROJECTION_COVERED",
                        "transformBy" : {
                                "y" : 1,
                                "_id" : 0
                        },
                        "inputStage" : {
                                "stage" : "IXSCAN",
                                "keyPattern" : {
                                        "x" : 1,
                                        "y" : 1
                                },
                                "indexName" : "x_1_y_1",
                                "isMultiKey" : false,
                                "multiKeyPaths" : {
                                        "x" : [ ],
                                        "y" : [ ]
                                },
                                "isUnique" : false,
                                "isSparse" : false,
                                "isPartial" : false,
                                "indexVersion" : 2,
                                "direction" : "forward",
                                "indexBounds" : {
                                        "x" : [
                                                "[4.0, 4.0]"
                                        ],
                                        "y" : [
                                                "[MinKey, MaxKey]"
                                        ]
                                }
                        }
                },
                "rejectedPlans" : [ ]
        },
        "serverInfo" : {
                "host" : "<//HOSTNAME_HERE//>",
                "port" : 27017,
                "version" : "4.2.0",
                "gitVersion" : "a4b751dcf51dd249c5865812b390cfd1c0129c30"
        },
        "ok" : 1
}
```



### 18.MongoDB 原子操作

MongoDB不支持事务，因此不管怎么设计数据库，都不要要求MongoDB可以保证数据完整性。

但MongoDB提供了许多原子操作，比如文档的保存，修改，删除等，都是原子操作。

原子操作：这个文档要么成功保存到MongoDB，要么没有保存到MongoDB中，不会出现查询到的文档没有保存完整的情况。

```shell
> use atomic
> db.books.insert({"name":"ABC","pages":200,"avail":5,checkout:[{by:"Ann"}]})
> db.books.findAndModify({
... query:{
... avail:{$gt:0}
... },
... update:{
... $inc:{avail:-1},
... $push:{checkout:{by:"abc"}}
...	}
...	})
{
	"_id":ObjectId("5d9af2e7df770897afb37d00"),
	"name":"ABC",
	"pages":200,
	"avail":5,
	"checkout":[
		{
			"by":"Ann"
		}
	]
}
> db.books.find()
{"_id":ObjectId("5d9af2e7df770897afb37d00"),"name":"ABC","pages":200,"avail":4,"checkout":[{"by":"Ann"},{"by":"abc"}]}
```

使用db.collection.findAndModify()方法判断书籍是否可以结算并更新新的结算信息

▲通过原子操作确保嵌入文档中的avail字段和checkout字段是同步更新的

⭐原子操作常用命令

- $set：用来指定一个键并更新键值，如果键不存在，则创建这个键并且插入键值

```shell
{ $set : { field : value } }
```

- $unset：用来删除一个键

```shell
{ $unset : { field : 1} }
```

- $inc：对文档的某个值为数字型（只能为满足要求的数字）的键进行增减操作

```shell
{ $inc : { field : value } }
```

- $push：把value追加到field里，field一定要数组类型

```shell
{ $push : { field : value } }
```

- $pushAll：同$push，只是一次可以追加多个值到一个数组字段内

```shell
{ $pushAll : { field : value_array } }
```

- $pull：从数组field内删除一个value值

```shell
{ $pull : { field : value } }
```

- $addToSet：增加一个值到数组，只有当这个值不在数组内才增加
- $pop：删除数组的第一个或最后一个元素

```shell
{ $pop : { field : 1 } }
```

- $rename：修改字段名称

```shell
{ $rename : { old_field_name : new_field_name } }
```

- $bit：位操作，integer类型

```shell
{ $bit : { field : {and : 5}}}
```



### 19.MongoDB 高级索引

考察user文档如下：

```shell
{"_id":ObjectId("5d9b0806df770897afb37d02"),"address":{"x":1,"y":2,"z":3},"tags":["music","cricket","blogs"],"name":"Ann"}
```

##### 19.1 索引数组字段

假设我们基于标签来检索用户，为此我们需要对集合中的数组 tags 建立索引。在数组中创建索引，需要对数组中的每个字段依次建立索引。所以在我们为数组 tags 创建索引时，会为 music、cricket、blogs三个值建立单独的索引。

```shell
> db.user.createIndex({"tags":1})
> db.user.find({tags:"cricket"})
{ "_id" : ObjectId("5d9b0806df770897afb37d02"), "address" : { "x" : 1, "y" : 2, "z" : 3 }, "tags" : [ "music", "cricket", "blogs" ], "name" : "Ann" }
> db.user.find({tags:"cricket"}).explain()
{
        "queryPlanner" : {
                "plannerVersion" : 1,
                "namespace" : "atomic.user",
                "indexFilterSet" : false,
                "parsedQuery" : {
                        "tags" : {
                                "$eq" : "cricket"
                        }
                },
                "queryHash" : "9D3B61A7",
                "planCacheKey" : "04C9997B",
                "winningPlan" : {
                        "stage" : "FETCH",
                        "inputStage" : {
                                "stage" : "IXSCAN",
                                "keyPattern" : {
                                        "tags" : 1
                                },
                                "indexName" : "tags_1",
                                "isMultiKey" : true,
                                "multiKeyPaths" : {
                                        "tags" : [
                                                "tags"
                                        ]
                                },
                                "isUnique" : false,
                                "isSparse" : false,
                                "isPartial" : false,
                                "indexVersion" : 2,
                                "direction" : "forward",
                                "indexBounds" : {
                                        "tags" : [
                                                "[\"cricket\", \"cricket\"]"
                                        ]
                                }
                        }
                },
                "rejectedPlans" : [ ]
        },
        "serverInfo" : {
                "host" : "<//HOSTNAME_HERE//>",
                "port" : 27017,
                "version" : "4.2.0",
                "gitVersion" : "a4b751dcf51dd249c5865812b390cfd1c0129c30"
        },
        "ok" : 1
}
```

##### 19.2 索引子文档字段

```shell
> db.user.createIndex({"address.x":1,"address.y":1,"address.z":1})
> db.user.find({"address.x":1})   //查询1
{ "_id" : ObjectId("5d9b0806df770897afb37d02"), "address" : { "x" : 1, "y" : 2, "z" : 3 }, "tags" : [ "music", "cricket", "blogs" ], "name" : "Ann" }
> db.user.find({"address.y":2,"address.x":1})   //查询2
{ "_id" : ObjectId("5d9b0806df770897afb37d02"), "address" : { "x" : 1, "y" : 2, "z" : 3 }, "tags" : [ "music", "cricket", "blogs" ], "name" : "Ann" }
> db.user.find({"address.y":2,"address.x":1,"address.z":3})   //查询3
{ "_id" : ObjectId("5d9b0806df770897afb37d02"), "address" : { "x" : 1, "y" : 2, "z" : 3 }, "tags" : [ "music", "cricket", "blogs" ], "name" : "Ann" }
```

▲假设我们需要通过x、y、z字段来检索文档，由于这些字段是子文档的字段，我们需要对子文档创建索引。

查询表达不一定遵循指定的索引顺序，MongoDB会自动优化，所以会支持上述三种查询。



### 20.MongoDB 索引限制

##### 20.1 额外开销

每个索引占据一定存储空间，在进行插入、更新和删除操作时也需要对索引进行操作。因此如果很少对集合使用读取操作，不建议用索引。

##### 20.2 内存使用

索引存储在内存当中，应确保索引的大小不超过内存限制。如果索引大小超过了内存限制，那么MongoDB会删除一些索引，这将导致性能下降。

##### 20.3 查询限制

索引不能被以下查询使用：

- 正则表达式及非操作符，如$nin，$not等
- 算术运算符，如$mod等
- $where 子句

▲建议经常使用explain()方法来检测语句是否使用索引

##### 20.4 索引键限制

Ver 2.6之后，如果现有的索引字段的值超过索引键的限制，MongoDB不会创建索引

##### 20.5 插入文档超过索引键限制

如果文档的索引字段值超过了索引键的限制，MongoDB不会将任何文档转换成索引的集合，与mongorestore和mongoimport工具类似。

##### 20.6 最大范围

- 集合中索引不能超过64个
- 索引名的长度不能超过128个字符
- 一个复合索引最多可以有31个字段



### 21.MongoDB Map-Reduce

Map-Reduce是一种计算模型，将大批量的工作（数据）分解（Map）执行，然后再将结果合并成最终结果（reduce），对大规模数据分析相当实用。

```shell
db.collection.mapReduce(
   function() {emit(key,value);},  //map 函数
   function(key,values) {return reduceFunction},   //reduce 函数
   {
      out: collection,
      query: document,
      sort: document,
      limit: number
   }
)
```

▲使用MapReduce要实现两个函数Map函数和Reduce函数，Map函数调用 `emit(key,value)`方法遍历集合中所有的记录，将key与value传递给Reduce函数进行处理。

Map函数必须调用 `emit(key,value)`返回键值对。

参数说明：

- map：映射函数，生成键值对序列，作为reduce函数参数。
- reduce：统计函数，把key-values变为key-value，把values数组变成一个单一的value值。
- out：统计结果存放集合，如果不指定就使用临时集合，客户端断开后自动删除。
- query：筛选条件。只有满足条件的文档才会调用map函数（query，limit，sort可随意组合）
- sort：和limit结合的sort排序参数，发往map函数前给文档排序，可优化分组机制。
- limit：发往map函数的文档数量的上限（如果没有limit，单独使用sort用处不大）

```shell
> db.orders.insert({c_id:"A1",amount:200,status:"A"})
> db.orders.insert({c_id:"A1",amount:300,status:"A"})
> db.orders.insert({c_id:"B4",amount:100,status:"A"})
> db.orders.insert({c_id:"A1",amount:150,status:"B"})
> db.orders.mapReduce(
... function(){emit(this.c_id,this.amount);},
... function(key,values){return Array.sum(values)},
...{
... query:{status:"A"},
... out:"order_totals"
... })
{
        "result" : "order_totals",
        "timeMillis" : 815,
        "counts" : {
                "input" : 3,
                "emit" : 3,
                "reduce" : 1,
                "output" : 2
        },
        "ok" : 1
}
> db.order_totals.find()
{"_id":"A1","value":500}
{"_id":"B4","value":100}
```

▲参数说明：

- result：储存结果的集合名称
- timeMillis：执行花费的时间，以毫秒为单位
- input：满足条件被发送到map函数的文档个数
- emit：在map函数中emit被调用的次数，即所有集合中的数据总量
- output：结果集合中的文档个数
- ok：是否成功，成功为1
- err：如果失败，这里可以有失败原因

MapReduce可被用来构建大型复杂的聚合查询，Map函数和Reduce函数可以使用JavaScript来实现，使得MapReduce非常灵活与强大。



### 22.MongoDB 全文检索

全文检索对每一个词建立一个索引，指明该词在文章中出现的次数和位置，当用户查询时，检索程序就根据事先建立的索引进行查找，并将查找的结果反馈给用户的检索方式。 这个过程类似于通过字典中的检索字表查字的过程。

##### 22.1 启用全文检索

Ver 2.6后默认开启全文检索

##### 22.2 创建全文索引

```shell
> db.text.insert({"text":"He is familiar with Java and Python","tags":["Java","Python"]})
> db.text.createIndex({text:"text"})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}
```

▲考察内容（text）和标签（tags），对text字段建立全文索引，进而我们可以搜索到文章内的内容。

##### 22.3 使用全文索引

```shell
> db.text.find({$text:{$search:"Java"}})
{ "_id" : ObjectId("5d9bfa37aad2a0ad8d191e3d"), "text" : "He is familiar with Java and Python", "tags" : [ "Java", "Python" ] }
```

▲使用全文索引提高搜索效率

##### 22.4 删除全文索引

```shell
> db.text.getIndexes()
[
        {
                "v" : 2,
                "key" : {
                        "_id" : 1
                },
                "name" : "_id_",
                "ns" : "test.text"
        },
        {
                "v" : 2,
                "key" : {
                        "_fts" : "text",
                        "_ftsx" : 1
                },
                "name" : "text_text",
                "ns" : "test.text",
                "weights" : {
                        "text" : 1
                },
                "default_language" : "english",
                "language_override" : "language",
                "textIndexVersion" : 3
        }
]
> db.text.dropIndex("text_text")
{ "nIndexesWas" : 2, "ok" : 1 }
```



### 23.MongoDB 正则表达式

正则表达式是用单个字符串来描述，匹配一系列复合某个句法规则的字符串。MongoDB 使用$regex操作符设置匹配字符串的正则表达式。MongoDB使用PCRE作为正则表达式语言。

```shell
{ "_id" : ObjectId("5d9bfa37aad2a0ad8d191e3d"), "text" : "He is familiar with Java and Python", "tags" : [ "Java", "Python" ] }
```

依然使用上面的text文档结构

```shell
> db.text.find({text:{$regex:"java"}})
> db.text.find({text:{$regex:"Java"}})   //查询1
{ "_id" : ObjectId("5d9bfa37aad2a0ad8d191e3d"), "text" : "He is familiar with Java and Python", "tags" : [ "Java", "Python" ] }
> db.text.find({text:/java/})
> db.text.find({text:/Java/})   //查询2
{ "_id" : ObjectId("5d9bfa37aad2a0ad8d191e3d"), "text" : "He is familiar with Java and Python", "tags" : [ "Java", "Python" ] }
> db.text.find({text:{$regex:"java",$options:"$i"}})   //查询3
{ "_id" : ObjectId("5d9bfa37aad2a0ad8d191e3d"), "text" : "He is familiar with Java and Python", "tags" : [ "Java", "Python" ] }
> db.text.find({tags:{$regex:"Ja"}})   //查询4
{ "_id" : ObjectId("5d9bfa37aad2a0ad8d191e3d"), "text" : "He is familiar with Java and Python", "tags" : [ "Java", "Python" ] }
> db.text.find({text:{$regex:"^He"}})   //查询5
{ "_id" : ObjectId("5d9bfa37aad2a0ad8d191e3d"), "text" : "He is familiar with Java and Python", "tags" : [ "Java", "Python" ] }
> db.text.find({text:{$regex:"hon$"}})   //查询6
{ "_id" : ObjectId("5d9bfa37aad2a0ad8d191e3d"), "text" : "He is familiar with Java and Python", "tags" : [ "Java", "Python" ] }
```

▲查询1和查询2有相同效果，但注意这时候需要确保大小写一致。

​	查询3设置了$options为$i，这时候检索不区分大小写。

​	查询4对数组元素使用正则表达式，可以查找以Ja开头的tags数据。

​	查询5将查找以He为开头的字符串。查询6将查找以hon为结尾的字符串。

⭐如果文档字段设置了索引，那么用索引相比于正则表达式匹配查找所有的数据的查询速度更快。



### 24.MongoDB 固定集合

Capped Collections：固定大小的集合，类似一个环形队列，当一个集合空间用完之后，再插入的元素就会覆盖最初始的头部元素。

##### 24.1 创建固定集合

```shell
> db.createCollection("cappedcollection",{capped:true,size:10000,max:1000})
{ "ok" : 1 }
> db.cappedcollection.isCapped()  //判断集合是否为固定集合
true
> db.runCommand({"convertToCapped":"text",size:10000})  //将已有集合转换为固定集合
{ "ok" : 1 }
> db.text.isCapped()
true
```

##### 24.2 固定集合查询

```shell
> db.text.find().sort({$natural:-1})
```

固定集合文档按照插入顺序储存，默认情况下查询就是按照插入顺序返回的，也可以使用$natural调整返回顺序。

##### 24.3 固定集合的功能特点，集合属性以及用法

功能特点：可以插入和更新，但更新不能超出collection大小，否则更新失败，不允许删除，但可以调用 `drop()`方法删除集合中所有行，但是 `drop()`之后要显式重建集合。

属性：

- 对固定集合进行插入速度极快
- 按照插入顺序的查询输出速度极快
- 能够在插入最新数据时，淘汰最早的数据

用法：

- 储存日志信息
- 缓存一些少量的文档



### 25.MongoDB 自动增长

MongoDB没有像SQL一样的自动增长功能，然而在某些情况下，我们可能需要实现ObjectId自动增长功能，但由于MongoDB没有实现这个功能，我们通过编程方式实现。以下我们在counters集合中实现 _id字段的自动增长。希望 _id字段实现从1，2，3，4到n的自动增长功能。

```shell
> db.products.insert({"_id":1,"p_name":"Apple","category":"mobiles"})
> db.createCollection("counters")
> db.counters.insert({_id:"productid",seq_value:0})
> function getNext(seqName){
... var seqDocument = db.counters.findAndModify(
... {
... query:{_id:seqName},
... update:{$inc:{seq_value:1}},
... "new":true
... });
... return seqDocument.seq_value;
... }
> db.products.insert({_id:getNext("productid"),"p_name":"Apple","category":"mobiles"})
WriteResult({
        "nInserted" : 0,
        "writeError" : {
                "code" : 11000,
                "errmsg" : "E11000 duplicate key error collection: test.products index: _id_ dup key: { _id: 1.0 }"
        }
})
>db.products.insert({"_id":getNext("productid"),"p_name":"SamSung","category":"mobiles"})
> db.products.find()
{ "_id" : 1, "p_name" : "Apple", "category" : "mobiles" }
{ "_id" : 2, "p_name" : "SamSung", "category" : "mobiles" }
```

▲counters集合中的seq_value字段是序列通过自动增长后的一个值。创建Javascript函数getNext来作为序列名输入，指定的序列会自动增长1并返回最新序列值。