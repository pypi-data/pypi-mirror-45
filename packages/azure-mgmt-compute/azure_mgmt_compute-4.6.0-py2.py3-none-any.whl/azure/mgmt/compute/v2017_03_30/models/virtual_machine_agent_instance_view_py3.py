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


class VirtualMachineAgentInstanceView(Model):
    """The instance view of the VM Agent running on the virtual machine.

    :param vm_agent_version: The VM Agent full version.
    :type vm_agent_version: str
    :param extension_handlers: The virtual machine extension handler instance
     view.
    :type extension_handlers:
     list[~azure.mgmt.compute.v2017_03_30.models.VirtualMachineExtensionHandlerInstanceView]
    :param statuses: The resource status information.
    :type statuses:
     list[~azure.mgmt.compute.v2017_03_30.models.InstanceViewStatus]
    """

    _attribute_map = {
        'vm_agent_version': {'key': 'vmAgentVersion', 'type': 'str'},
        'extension_handlers': {'key': 'extensionHandlers', 'type': '[VirtualMachineExtensionHandlerInstanceView]'},
        'statuses': {'key': 'statuses', 'type': '[InstanceViewStatus]'},
    }

    def __init__(self, *, vm_agent_version: str=None, extension_handlers=None, statuses=None, **kwargs) -> None:
        super(VirtualMachineAgentInstanceView, self).__init__(**kwargs)
        self.vm_agent_version = vm_agent_version
        self.extension_handlers = extension_handlers
        self.statuses = statuses
