import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
import pandas as pd
import logging

CosmosClient = None
database = None
container = None

def load_ipython_extension(ipython):
    global database, container, CosmosClient
    import os
    host = os.environ["COSMOS_ENDPOINT"]
    masterkey = os.environ["COSMOS_MASTERKEY"]
    print(host)

    if host is None or masterkey is None:
        logging.error("Cosmos endpoint credentials is not set.")
        print("cosmos endpoint credentials is not set")

    CosmosClient = cosmos_client.CosmosClient(host, {'masterKey': masterkey})
    ipython.register_magics(CosmosMagics)

def unload_ipython_extension(ipython):
    CosmosClient = None
    pass

@magics_class
class CosmosMagics(Magics):
    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--database', '-d',
      help='specifies database name'
    )
    @magic_arguments.argument('--container', '-c',
      help='specifies container name'
    )
    def sql(self, line='', cell=None):
        global database, container, CosmosClient

        args = magic_arguments.parse_argstring(self.sql, line)

        if args.database:
            database_id = args.database
        else:
            database_id = database
        if args.container:
            container_id = args.container
        else:
            container_id = container

        database_link = 'dbs/' + database_id
        earthquakes = database_link + '/colls/' + container_id
        query = {"query": cell}
        items = list(CosmosClient.QueryItems(earthquakes, query, {'enableCrossPartitionQuery': True}))
        df = pd.DataFrame.from_records(items)
        return df

    @line_magic("database")
    def set_database(self, line, cell="", local_ns=None):
        print("Using database " + line)
        global database, container, CosmosClient
        database = line

    @line_magic("container")
    def set_container(self, line, cell="", local_ns=None):
        print("Using container " + line)
        global database, container, CosmosClient
        container = line