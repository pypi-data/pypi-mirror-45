# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Step(Model):
    """The properties that define an Azure Deployment Manager step.

    All required parameters must be populated in order to send to Azure.

    :param name: Required. The name of the step group.
    :type name: str
    :param depends_on_step_groups: The list of step group names on which this
     step group depends on.
    :type depends_on_step_groups: list[str]
    :param pre_deployment_steps: The list of steps to be run before deploying
     the target.
    :type pre_deployment_steps:
     list[~azure.mgmt.deploymentmanager.models.PrePostStep]
    :param deployment_target_id: Required. The resource Id of service unit to
     be deployed. The service unit should be from the service topology
     referenced in targetServiceTopologyId
    :type deployment_target_id: str
    :param post_deployment_steps: The list of steps to be run after deploying
     the target.
    :type post_deployment_steps:
     list[~azure.mgmt.deploymentmanager.models.PrePostStep]
    """

    _validation = {
        'name': {'required': True},
        'deployment_target_id': {'required': True},
    }

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'depends_on_step_groups': {'key': 'dependsOnStepGroups', 'type': '[str]'},
        'pre_deployment_steps': {'key': 'preDeploymentSteps', 'type': '[PrePostStep]'},
        'deployment_target_id': {'key': 'deploymentTargetId', 'type': 'str'},
        'post_deployment_steps': {'key': 'postDeploymentSteps', 'type': '[PrePostStep]'},
    }

    def __init__(self, **kwargs):
        super(Step, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.depends_on_step_groups = kwargs.get('depends_on_step_groups', None)
        self.pre_deployment_steps = kwargs.get('pre_deployment_steps', None)
        self.deployment_target_id = kwargs.get('deployment_target_id', None)
        self.post_deployment_steps = kwargs.get('post_deployment_steps', None)
