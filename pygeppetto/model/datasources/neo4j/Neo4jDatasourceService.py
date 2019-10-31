from pygeppetto.services.data_source_service import DataSourceService
from .Neo4jResponseProcessor import Neo4jResponseProcessor

class Neo4jDataSourceService(DataSourceService):
    def get_connection_type(self):
        return "POST"

    def get_query_response_processor(self):
        if not hasattr(self, "query_response_processor"):
            self.query_response_processor = Neo4jResponseProcessor()
        return self.query_response_processor