# ipython-cosmos-extension
IPython Extension for Cosmos SQL

##Install the extension:
    
    !pip install  ipython-cosmos-extension

##Load the extension:
  
  This extension assumes cosmosdb endpoint credentials
  are set as environment variables accessable by
  ``COSMOS_ENDPOINT`` and ``COSMOS_MASTERKEY``.
  
    %load_ext cosmos_sql
  
## Set Database name
    %database <your_database_name>
     
## Set Container name     
    %container <your_container_name>
    
##Execute Cosmos SQL Statements
    %sql select * from user;
    
##Auto conversion of result to data frame
   To disable auto conversion of result to dataframe:
   
    %disable_autoconvert_to_dataframe 

   Enabling auto conversion of result to dataframe:
   
    %enable_autoconvert_to_dataframe 


