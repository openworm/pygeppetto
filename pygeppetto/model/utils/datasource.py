from pygeppetto.model.datasources import Query


def query_check(query: Query, types=()) -> bool:
    """
    https://github.com/openworm/org.geppetto.core/blob/master/src/main/java/org/geppetto/core/datasources/QueryChecker.java)
    :return:
    """
    if len(query.matchingCriteria) == 0:
        return True

    all_types = set()
    all_types.update(types)

    for criterion in query.matchingCriteria:
        for type_to_match in criterion.type:
            if not type_to_match in all_types:
                for type_ in all_types:
                    if type_.extends_type(type_to_match):
                        return True
    return False

