# ipython-cosmos-extension
IPython Extension for Cosmos SQL

## Install the extension:

```bash
    !pip install  ipython-cosmos-extension
```

## Load the extension:
  
  This extension assumes cosmosdb endpoint credentials
  are set as environment variables accessable by
  ``COSMOS_ENDPOINT`` and ``COSMOS_MASTERKEY``.
  
```bash
    %load_ext cosmos_sql
```
    
## Set Database name

```bash
    %database <your_database_name>
```

## Set Container name     
```bash
    %container <your_container_name>
```
    
## Execute Cosmos SQL Statements
```bash
    %sql select * from user;
```

To get the result from the command use ``_`` variable.
    
## Auto conversion of result to data frame
   To disable auto conversion of result to dataframe:
```bash
    %disable_autoconvert_to_dataframe 
```

   Enabling auto conversion of result to dataframe:
```bash
    %enable_autoconvert_to_dataframe 
```


