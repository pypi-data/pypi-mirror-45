import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
import pandas as pd

def load_ipython_extension(ipython):
    ipython.register_magics(CosmosMagics)

def unload_ipython_extension(ipython):
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
    @magic_arguments.argument('--host',
      help='specifies host endpoint'
    )
    @magic_arguments.argument('--masterKey',
      help='specifies masterKey'
    )
    def sql(self, line='', cell=None):
        args = magic_arguments.parse_argstring(self.sql, line)
        DATABASE_ID = args.database
        COLLECTION_ID = args.container

        host = args.host
        key = args.masterKey

        print("host is " + host)
        CosmosClient = cosmos_client.CosmosClient(host, {'masterKey': key})

        database_link = 'dbs/' + DATABASE_ID
        earthquakes = database_link + '/colls/' + COLLECTION_ID
        query = {"query": cell}
        items = list(CosmosClient.QueryItems(earthquakes, query, {'enableCrossPartitionQuery': True}))
        df = pd.DataFrame.from_records(items)
        return df


