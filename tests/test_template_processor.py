import pytest
from pygeppetto.model.utils import template

def test_template_processor():
    query = "MATCH(n) WHERE id(n)=$ID RETURN id(n) as ID, n;"

    output = template.process_template(template='{"statement":"$QUERY"}',
                                       ID="visitor", QUERY=query)

    assert output == "{\"statement\":\"MATCH(n) WHERE id(n)=visitor RETURN id(n) as ID, n;\"}"
