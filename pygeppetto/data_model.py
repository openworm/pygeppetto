class GeppettoProject(object):

    def __init__(self, id, name, geppetto_model, volatile=True, base_url=None, public=False, experiments=None,
                 view=None):
        self.id = id
        self.name = name
        self.geppettoModel = geppetto_model  # Beware must use the camelCase here otherwise we cannot import from JSON
        self.base_url = base_url
        self.experiments = list(experiments) if experiments is not None else []
        self.active_experiment_id = -1 if not experiments else 0
        self.volatile = volatile
        self.view = view
        self.is_public = public

    def __eq__(self, o: object) -> bool:
        return self.id == o.id if hasattr(o, 'id') else False

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return "GeppettoProject[id={}, name={}]".format(self.id, self.name)


