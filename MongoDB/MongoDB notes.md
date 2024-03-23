# **Introduction**

- MongoDB is a noSQL DB where
  
  - no joins but can `ref = User`

## Advantages:

- Easy to iterate and change schemas

- Horizontally more scalable and better for performance

- Object-Oriented -- looks ~ JS code

- Better for Agile development
  
  - Accomodates large volumes of rapidly changing structured, semi-structured and unstructured

```mongodb
OldUser Schema
{
    "first": "larry"
    "last": "david"
}

NewUser Schema
{
    "first": "larry"
    "last": "david"
    "number": 5559090
}
```

## Documents And Collection

### Documents

A record in a MongoDB collection and the basic unit of data in MongoDB. Documents look like JSON objects but exists in `BSON`.

The main difference between BSON and JSON:

```mongodb
{
    "first": "larry"
    "last": "david"
}
```

- quotes around both key and value pair

```json
{
 first: "larry"
 last: "david"
}
```

- no quotes around keys required

### Collection

A grouping of MongoDB documents. Typically, all documents in a collection have a similar or related purpose.

> make sure to download both   `mongoshell` and `mongodb server connection` 
> 
> Can also use MongoDB compass to use GUI to do the following

# **MongoDB commands**

Navigate to you `C:\Program Files\MongoDB\Server\3.2\bin` and then initiate mongodb as following

- you will need    `mongod.exe` for starting the server and `mongosh.exe` for starting the shell

```powershell
mongod
# starts the connection 
mongosh
```

Then we can now just use `mongo` to access the shell

## Most common commands:

In `mongoshell` you can type:

```mongodb
show dbs # show all databases present
use db_name # switch to that database
show collections # shows all the connections in it 
db.collection.find() # show content of the collections
```

Example of such a command:

```mongodb
local> show dbs
admin    40.00 KiB
config  108.00 KiB
local    72.00 KiB
trial     8.00 KiB
local> use trial
switched to db trial
trial> show collections
temp
trial> db.temp.find()
[ { _id: ObjectId('65fe71df7c00c2cc1d41b1fd'), number: '42069' } ]
```

<img title="" src="file:///C:/MINE/NERD STUFF/new skills/Fullstack ML-AI/LEARNING_practical_dsci/MongoDB/MongoDB compass.png" alt="">

<img title="" src="file:///C:/MINE/NERD STUFF/new skills/Fullstack ML-AI/LEARNING_practical_dsci/MongoDB/mongoshell.png" alt="">

Showing both ways of accessing data above

We can directly use JSON to insert into mongoDB

## More commands

```mongodb
#### self explanatory
db.createCollection("car")

#### inserts a document into the collection
db.car.insert({
    name: 'honda',
    make: 'accord',
    year: '2010'
}) 

#### shows the docs in above format
db.car.find().pretty() 

##### updated the name of the document
db.car.update({
    name: 'honda'
},
{$set{
     name: 'ford'   
}
}) 


#### add a feature to the document
db.car.update({
    name: 'ford'
},
{$set{
     transmission: 'automatic'   
}},{$upsert:true}) 


#### remove documents that satisfy the following feature
db.car.remove({name:"ford"})


#### can run JS scripts too
for(var i = 0; i < 10; i++){
    db.things.insert({"x":i})
}
```



# **Working with Data**



## Data Types



There are following data types:

```mongodb
/*1:=======================================================*/
name:string{
    name:"john"
}

/*2:=======================================================*/
likes:Number{
    likes:5
}

/*3:=======================================================*/
ETL_timestamp:Date{
    ETL_timestamp:ISODate("...")
}

/*4:=======================================================*/
tags:Array
OR
tags[]
{
    tags:["tag1","tag2"]
}


/*5:=======================================================*/
published:Boolean{
    published:true
}


/*6:=======================================================*/
/*=======Collection of/ references Other data types========*/
_creator:Schema.ObjectId{
    _creator:"41239878"
}
```

- We also have `Buffer` used for *Video, Images and Audio*

- We also have `Mixed` which *combines different types*



## Query Data

We can find all the documents the normal way:



### Finding

```mongodb
/* get all the docs in nice format*/
db.collection.pretty() 

/* get all the data w/ this property, ~ WHERE */
db.collection.find({'name':'Rachel'}) 

/* find values greater than, gt, or lesser than, lt */
db.student.find({unit: {$gt 6})
db.student.find({unit: {$lt 6})

/* checks for something in an array, checks intersection of whol arr*/
db.student.find({classes: {$in ['history', 'geography']})
```



### Sorting

```mongodb
/* sorts numerically ascending for units, after the $in filter */
db.student.find({classes: {$in ['history', 'geography']}).sort({units: -1})

/* sorts alphabetically descending for name, ~ ORDER BY */
db.student.find({}).sort({name: 1})

/* top 2 of sorts alphabetically descending for name, ~ LIMIT or TOP */
db.student.find({}).sort({name:1}).limit(2)


```



Can find more commands at [mongodb commands](https://www.mongodb.com/docs/mongodb-shell/)


