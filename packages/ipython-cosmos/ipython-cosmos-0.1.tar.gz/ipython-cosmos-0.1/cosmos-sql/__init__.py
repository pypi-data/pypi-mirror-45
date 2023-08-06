from IPython.core.magic import Magics, magics_class, cell_magic, line_magic, needs_local_scope
from IPython.config.configurable import Configurable
import azure.cosmos.cosmos_client as cosmos_client

@magics_class
class TestMagics(Magics):
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
        CosmosClient = cosmos_client.CosmosClient(host, {'masterKey': key})
        args = magic_arguments.parse_argstring(self.sql, line)
        DATABASE_ID = args.database
        COLLECTION_ID = args.container
        database_link = 'dbs/' + DATABASE_ID
        earthquakes = database_link + '/colls/' + COLLECTION_ID
        query = {"query": cell}
        items = list(CosmosClient.QueryItems(earthquakes, query, {'enableCrossPartitionQuery': True}))
        df = pd.DataFrame.from_records(items)
        return df