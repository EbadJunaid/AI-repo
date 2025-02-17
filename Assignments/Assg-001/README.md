
# Assignment-01 (CNIC's Hashmaps) 


## Original Problem Statement

Create a hashmap for CNIC. It should cater only those CNICs which have the same first 4 digits as your CNIC. Give hash function, data structure, average and maximum number of collisions, collision resolution approach.


## How I approach the problem ?


- First I am creating a function which is generating different variations of the CNIC's starting with prefix string and it creates the count number of CNIC . It can contain duplicate CNIC's but that does not matter because this is just for testing purposes.

- As we read from the file so each CNIC is string so we create a simple hash function which does hashing based on the remaining character excluding the prefix. For example if `CNIC = 3530154082498` and `prefix = 3530` then it does hashing on the remaining characters which are `154082498`.

- To handle the collisions we simply use the chaining method which is simply a vector 

- It has below functions :

    - Insert 
    - Contains (find)
    - getCollisionStats (Tell about maximum and average collisions)


## Compiling the code :

Use the below command to run the code 

```make
  make
```
    
This command will create all the executables(binaries)

## Running the code :

Use the below command to run the code 

```make
  make run 
```

## Clean the executables :
```make
  make clean
```

## 🚀 About Me
I'm just a below average programmer



