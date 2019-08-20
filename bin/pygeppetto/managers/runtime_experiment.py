from pygeppetto.model import ExperimentState


class RuntimeExperiment(object):
    def __init__(self, project, experiment):
        self.project = project
        self.experiment = experiment
        self.state = ExperimentState()

    def get_experiment_state(self, variables, url_base):
        pass
