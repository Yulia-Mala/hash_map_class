## Hash Map class 

***Allow us to store associative array with average O(1) access time***

Create your empty HashMap or use iterable to add pairs:
```
 my_map = HashMap()

 my_map = HashMap(
  [
    [key1, value1], 
    [key2, value2],
    ...
  ]
)
```

Two types of syntax are realized:

1) Use the [] (indexer) operators:
  -  Assignment: ``` my_map[key] = value ```
  -  Retrieving: ``` print(my_map[key]) ```
  -  Deletion: ``` del my_map[key] ```  
  
In case of trying to delete or retrieve non-existing value KeyError would occure

2) Use methods:
 - Assignment: ``` my_map.put(key=key, value=value)```
-  Retrieving: ``` print(my_map(key=key, default=defaulf_value)) ```  

You could specify the default value witch would be returned if such a key doesn't exist  
Default value of this parameter is None
