import json
import logging

from pygeppetto.model import QueryResults
from pygeppetto.model.datasources import QueryResult
from pygeppetto.services.data_source_service import DataSourceService

NEO4J_ERROR_PARSING_RESPONSE = "Error parsing Neo4j response"
NEO4J_ERROR_MISSING_COLUMN_KEY_IN_RESPONSE = "Missing `columns` key in Neo4j response."
NEO4J_ERROR_MISSING_ROW_KEY_IN_RESPONSE = "Missing `row` or `meta` key in Neo4j response."
NEO4J_ERROR_MISSING_ERROR_KEY_IN_RESPONSE = 'Neo4j: missing "error" key in Neo4j response.'

NEO4J_ROW_KEY = "row"
NEO4J_META_KEY = "meta"
NEO4J_DATA_KEY = "data"
NEO4J_ERRORS_KEY = "errors"
NEO4J_RESULTS_KEY = "results"
NEO4J_COLUMNS_KEY = "columns"

TEMPLATE = '''{
  "statements":[
    {
      $QUERY,
      "resultDataContents":[
        "row"
      ],
      "includeStats":false
    }
  ]
}'''


class Neo4jDataSourceService(DataSourceService):

    def get_connection_type(self):
        return "POST"

    def get_template(self):
        return TEMPLATE

    def process_response(self, response):
        query_results = QueryResults(header=[], results=[])

        for chunk in response:
            try:
                chunk = json.loads(chunk)
            except:
                logging.error(chunk)
                raise Exception(NEO4J_ERROR_PARSING_RESPONSE)

            if NEO4J_ERRORS_KEY in chunk and not chunk[NEO4J_ERRORS_KEY]:
                for container in chunk[NEO4J_RESULTS_KEY]:
                    if NEO4J_COLUMNS_KEY in container:
                        query_results.header.update(container[NEO4J_COLUMNS_KEY])
                    else:
                        logging.error(NEO4J_ERROR_MISSING_COLUMN_KEY_IN_RESPONSE)
                        break

                    for data in container[NEO4J_DATA_KEY]:
                        if NEO4J_ROW_KEY in data and NEO4J_META_KEY in data:
                            # can't store r as dict because it is unhashable
                            row = [json.dumps(r) for r in data[NEO4J_ROW_KEY]]
                            query_results.results.append(QueryResult(values=row))
                        else:
                            logging.error(NEO4J_ERROR_MISSING_ROW_KEY_IN_RESPONSE)
                            break
            else:
                if not NEO4J_ERRORS_KEY in chunk:
                    logging.error(NEO4J_ERROR_MISSING_ERROR_KEY_IN_RESPONSE)
                else:
                    for error in chunk[NEO4J_ERRORS_KEY]:
                        logging.error('Neo4j: error_code %s, error_message: %s.',
                                      error["code"], error["message"])

        return query_results
