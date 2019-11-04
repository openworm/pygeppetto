import airspeed

def process_template(template, **properties):
    target = template
    tpl = airspeed.Template(target)
    result = tpl.merge(properties)
    if '$' in target and result != template:
        return process_template(result, **properties)
    return result
