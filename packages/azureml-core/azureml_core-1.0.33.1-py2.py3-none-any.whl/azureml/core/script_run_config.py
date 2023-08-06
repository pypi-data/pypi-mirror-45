# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Class for handling script run configuration."""

from azureml._base_sdk_common.tracking import global_tracking_info_registry
from azureml._logging import ChainedIdentity
from ._experiment_method import experiment_method
from .runconfig import RunConfiguration


def submit(script_run_config, workspace, experiment_name):
    """Submit and return the run.

    :param script_run_config:
    :type script_run_config:  azureml.core.script_run_config.ScriptRunConfig
    :param workspace:
    :type workspace: azureml.core.workspace.Workspace
    :param experiment_name:
    :type experiment_name: str
    :return: Returns the run.
    :rtype: azureml.core.script_run.ScriptRun
    """
    from azureml.core import Experiment
    from azureml._execution import _commands
    from azureml._project.project import Project

    experiment = Experiment(workspace, experiment_name)
    project = Project(directory=script_run_config.source_directory, experiment=experiment)

    run_config = get_run_config_from_script_run(script_run_config)

    run = _commands.start_run(project, run_config,
                              telemetry_values=script_run_config._telemetry_values)
    run.add_properties(global_tracking_info_registry.gather_all(script_run_config.source_directory))

    return run


def get_run_config_from_script_run(script_run_config):
    """Get RunConfiguration object with parameters copied from the ScriptRunConfig.

    :param script_run_config:
    :type script_run_config:  azureml.core.script_run_config.ScriptRunConfig
    :return: Return the run configuration.
    :rtype: azureml.core.runconfig.RunConfiguration
    """
    # Gets a deep copy of run_config
    run_config = RunConfiguration._get_run_config_object(
        path=script_run_config.source_directory, run_config=script_run_config.run_config)

    if script_run_config.arguments:
        run_config.arguments = script_run_config.arguments

    if script_run_config.script:
        run_config.script = script_run_config.script

    return run_config


class ScriptRunConfig(ChainedIdentity):
    """A class for setting up configurations for script runs. Type: ChainedIdentity.

    :param source_directory:
    :type source_directory: str
    :param script:
    :type script: str
    :param arguments:
    :type arguments: :class:`list`
    :param run_config:
    :type run_config: azureml.core.runconfig.RunConfiguration
    :param _telemetry_values:
    :type _telemetry_values: dict
    """

    @experiment_method(submit_function=submit)
    def __init__(self, source_directory, script=None, arguments=None, run_config=None, _telemetry_values=None):
        """Class ScriptRunConfig constructor.

        :type source_directory: str
        :type script: str
        :type arguments: :class:`list`
        :type run_config: azureml.core.runconfig.RunConfiguration
        """
        self.source_directory = source_directory
        self.script = script
        self.arguments = arguments
        self.run_config = run_config if run_config else RunConfiguration()
        self._telemetry_values = _telemetry_values
