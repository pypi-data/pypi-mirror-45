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

from .resource_py3 import Resource


class VirtualMachine(Resource):
    """Describes a Virtual Machine.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    All required parameters must be populated in order to send to Azure.

    :ivar id: Resource Id
    :vartype id: str
    :ivar name: Resource name
    :vartype name: str
    :ivar type: Resource type
    :vartype type: str
    :param location: Required. Resource location
    :type location: str
    :param tags: Resource tags
    :type tags: dict[str, str]
    :param plan: Specifies information about the marketplace image used to
     create the virtual machine. This element is only used for marketplace
     images. Before you can use a marketplace image from an API, you must
     enable the image for programmatic use.  In the Azure portal, find the
     marketplace image that you want to use and then click **Want to deploy
     programmatically, Get Started ->**. Enter any required information and
     then click **Save**.
    :type plan: ~azure.mgmt.compute.v2016_03_30.models.Plan
    :param hardware_profile: Specifies the hardware settings for the virtual
     machine.
    :type hardware_profile:
     ~azure.mgmt.compute.v2016_03_30.models.HardwareProfile
    :param storage_profile: Specifies the storage settings for the virtual
     machine disks.
    :type storage_profile:
     ~azure.mgmt.compute.v2016_03_30.models.StorageProfile
    :param os_profile: Specifies the operating system settings for the virtual
     machine.
    :type os_profile: ~azure.mgmt.compute.v2016_03_30.models.OSProfile
    :param network_profile: Specifies the network interfaces of the virtual
     machine.
    :type network_profile:
     ~azure.mgmt.compute.v2016_03_30.models.NetworkProfile
    :param diagnostics_profile: Specifies the boot diagnostic settings state.
     <br><br>Minimum api-version: 2015-06-15.
    :type diagnostics_profile:
     ~azure.mgmt.compute.v2016_03_30.models.DiagnosticsProfile
    :param availability_set: Specifies information about the availability set
     that the virtual machine should be assigned to. Virtual machines specified
     in the same availability set are allocated to different nodes to maximize
     availability. For more information about availability sets, see [Manage
     the availability of virtual
     machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-manage-availability?toc=%2fazure%2fvirtual-machines%2fwindows%2ftoc.json).
     <br><br> For more information on Azure planned maintenance, see [Planned
     maintenance for virtual machines in
     Azure](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-planned-maintenance?toc=%2fazure%2fvirtual-machines%2fwindows%2ftoc.json)
     <br><br> Currently, a VM can only be added to availability set at creation
     time. An existing VM cannot be added to an availability set.
    :type availability_set: ~azure.mgmt.compute.v2016_03_30.models.SubResource
    :ivar provisioning_state: The provisioning state, which only appears in
     the response.
    :vartype provisioning_state: str
    :ivar instance_view: The virtual machine instance view.
    :vartype instance_view:
     ~azure.mgmt.compute.v2016_03_30.models.VirtualMachineInstanceView
    :param license_type: Specifies that the image or disk that is being used
     was licensed on-premises. This element is only used for images that
     contain the Windows Server operating system. <br><br> Possible values are:
     <br><br> Windows_Client <br><br> Windows_Server <br><br> If this element
     is included in a request for an update, the value must match the initial
     value. This value cannot be updated. <br><br> For more information, see
     [Azure Hybrid Use Benefit for Windows
     Server](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-hybrid-use-benefit-licensing?toc=%2fazure%2fvirtual-machines%2fwindows%2ftoc.json)
     <br><br> Minimum api-version: 2015-06-15
    :type license_type: str
    :ivar vm_id: Specifies the VM unique ID which is a 128-bits identifier
     that is encoded and stored in all Azure IaaS VMs SMBIOS and can be read
     using platform BIOS commands.
    :vartype vm_id: str
    :ivar resources: The virtual machine child extension resources.
    :vartype resources:
     list[~azure.mgmt.compute.v2016_03_30.models.VirtualMachineExtension]
    :param identity: The identity of the virtual machine, if configured.
    :type identity:
     ~azure.mgmt.compute.v2016_03_30.models.VirtualMachineIdentity
    """

    _validation = {
        'id': {'readonly': True},
        'name': {'readonly': True},
        'type': {'readonly': True},
        'location': {'required': True},
        'provisioning_state': {'readonly': True},
        'instance_view': {'readonly': True},
        'vm_id': {'readonly': True},
        'resources': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'plan': {'key': 'plan', 'type': 'Plan'},
        'hardware_profile': {'key': 'properties.hardwareProfile', 'type': 'HardwareProfile'},
        'storage_profile': {'key': 'properties.storageProfile', 'type': 'StorageProfile'},
        'os_profile': {'key': 'properties.osProfile', 'type': 'OSProfile'},
        'network_profile': {'key': 'properties.networkProfile', 'type': 'NetworkProfile'},
        'diagnostics_profile': {'key': 'properties.diagnosticsProfile', 'type': 'DiagnosticsProfile'},
        'availability_set': {'key': 'properties.availabilitySet', 'type': 'SubResource'},
        'provisioning_state': {'key': 'properties.provisioningState', 'type': 'str'},
        'instance_view': {'key': 'properties.instanceView', 'type': 'VirtualMachineInstanceView'},
        'license_type': {'key': 'properties.licenseType', 'type': 'str'},
        'vm_id': {'key': 'properties.vmId', 'type': 'str'},
        'resources': {'key': 'resources', 'type': '[VirtualMachineExtension]'},
        'identity': {'key': 'identity', 'type': 'VirtualMachineIdentity'},
    }

    def __init__(self, *, location: str, tags=None, plan=None, hardware_profile=None, storage_profile=None, os_profile=None, network_profile=None, diagnostics_profile=None, availability_set=None, license_type: str=None, identity=None, **kwargs) -> None:
        super(VirtualMachine, self).__init__(location=location, tags=tags, **kwargs)
        self.plan = plan
        self.hardware_profile = hardware_profile
        self.storage_profile = storage_profile
        self.os_profile = os_profile
        self.network_profile = network_profile
        self.diagnostics_profile = diagnostics_profile
        self.availability_set = availability_set
        self.provisioning_state = None
        self.instance_view = None
        self.license_type = license_type
        self.vm_id = None
        self.resources = None
        self.identity = identity
