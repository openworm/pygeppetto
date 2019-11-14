from pygeppetto.model import GeppettoModel
from pygeppetto.model.exceptions import GeppettoModelException


class QueryNotFoundException(GeppettoModelException): pass


def get_query(query_path, model: GeppettoModel):
    data_source = None
    for token in query_path.split('.'):
        if data_source is None:
            try:
                return next(query for query in model.queries if query.id == token)
            except StopIteration:
                try:
                    data_source = next(ds for ds in model.dataSources if ds.id == token)
                except StopIteration:
                    raise QueryNotFoundException("Query `{}` not found in model.".format(query_path))
        else:
            try:
                return next(query for query in data_source.queries if query.id == token)
            except StopIteration:
                raise QueryNotFoundException("Query `{}` not found in model.".format(query_path))
    else:
        raise QueryNotFoundException("Query `{}` not found in model.".format(query_path))
