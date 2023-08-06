
# AUTO-GENERATED file from IFMapApiGenerator. Do Not Edit!

from contrail_heat.resources import contrail
try:
    from heat.common.i18n import _
except ImportError:
    pass
from heat.engine import attributes
from heat.engine import constraints
from heat.engine import properties
try:
    from heat.openstack.common import log as logging
except ImportError:
    from oslo_log import log as logging
import uuid

from vnc_api import vnc_api

LOG = logging.getLogger(__name__)


class ContrailVirtualRouter(contrail.ContrailResource):
    PROPERTIES = (
        NAME, FQ_NAME, DISPLAY_NAME, VIRTUAL_ROUTER_IP_ADDRESS, VIRTUAL_ROUTER_DPDK_ENABLED, PERMS2, PERMS2_OWNER, PERMS2_OWNER_ACCESS, PERMS2_GLOBAL_ACCESS, PERMS2_SHARE, PERMS2_SHARE_TENANT, PERMS2_SHARE_TENANT_ACCESS, VIRTUAL_ROUTER_TYPE, ANNOTATIONS, ANNOTATIONS_KEY_VALUE_PAIR, ANNOTATIONS_KEY_VALUE_PAIR_KEY, ANNOTATIONS_KEY_VALUE_PAIR_VALUE, VIRTUAL_MACHINE_REFS, NETWORK_IPAM_REFS, NETWORK_IPAM_REFS_DATA, NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_START, NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_END, NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_VROUTER_SPECIFIC_POOL, NETWORK_IPAM_REFS_DATA_SUBNET, NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX, NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX_LEN, SUB_CLUSTER_REFS, TAG_REFS, GLOBAL_SYSTEM_CONFIG
    ) = (
        'name', 'fq_name', 'display_name', 'virtual_router_ip_address', 'virtual_router_dpdk_enabled', 'perms2', 'perms2_owner', 'perms2_owner_access', 'perms2_global_access', 'perms2_share', 'perms2_share_tenant', 'perms2_share_tenant_access', 'virtual_router_type', 'annotations', 'annotations_key_value_pair', 'annotations_key_value_pair_key', 'annotations_key_value_pair_value', 'virtual_machine_refs', 'network_ipam_refs', 'network_ipam_refs_data', 'network_ipam_refs_data_allocation_pools', 'network_ipam_refs_data_allocation_pools_start', 'network_ipam_refs_data_allocation_pools_end', 'network_ipam_refs_data_allocation_pools_vrouter_specific_pool', 'network_ipam_refs_data_subnet', 'network_ipam_refs_data_subnet_ip_prefix', 'network_ipam_refs_data_subnet_ip_prefix_len', 'sub_cluster_refs', 'tag_refs', 'global_system_config'
    )

    properties_schema = {
        NAME: properties.Schema(
            properties.Schema.STRING,
            _('NAME.'),
            update_allowed=True,
            required=False,
        ),
        FQ_NAME: properties.Schema(
            properties.Schema.STRING,
            _('FQ_NAME.'),
            update_allowed=True,
            required=False,
        ),
        DISPLAY_NAME: properties.Schema(
            properties.Schema.STRING,
            _('DISPLAY_NAME.'),
            update_allowed=True,
            required=False,
        ),
        VIRTUAL_ROUTER_IP_ADDRESS: properties.Schema(
            properties.Schema.STRING,
            _('VIRTUAL_ROUTER_IP_ADDRESS.'),
            update_allowed=True,
            required=False,
        ),
        VIRTUAL_ROUTER_DPDK_ENABLED: properties.Schema(
            properties.Schema.BOOLEAN,
            _('VIRTUAL_ROUTER_DPDK_ENABLED.'),
            update_allowed=True,
            required=False,
        ),
        PERMS2: properties.Schema(
            properties.Schema.MAP,
            _('PERMS2.'),
            update_allowed=True,
            required=False,
            schema={
                PERMS2_OWNER: properties.Schema(
                    properties.Schema.STRING,
                    _('PERMS2_OWNER.'),
                    update_allowed=True,
                    required=False,
                ),
                PERMS2_OWNER_ACCESS: properties.Schema(
                    properties.Schema.INTEGER,
                    _('PERMS2_OWNER_ACCESS.'),
                    update_allowed=True,
                    required=False,
                    constraints=[
                        constraints.Range(0, 7),
                    ],
                ),
                PERMS2_GLOBAL_ACCESS: properties.Schema(
                    properties.Schema.INTEGER,
                    _('PERMS2_GLOBAL_ACCESS.'),
                    update_allowed=True,
                    required=False,
                    constraints=[
                        constraints.Range(0, 7),
                    ],
                ),
                PERMS2_SHARE: properties.Schema(
                    properties.Schema.LIST,
                    _('PERMS2_SHARE.'),
                    update_allowed=True,
                    required=False,
                    schema=properties.Schema(
                        properties.Schema.MAP,
                        schema={
                            PERMS2_SHARE_TENANT: properties.Schema(
                                properties.Schema.STRING,
                                _('PERMS2_SHARE_TENANT.'),
                                update_allowed=True,
                                required=False,
                            ),
                            PERMS2_SHARE_TENANT_ACCESS: properties.Schema(
                                properties.Schema.INTEGER,
                                _('PERMS2_SHARE_TENANT_ACCESS.'),
                                update_allowed=True,
                                required=False,
                                constraints=[
                                    constraints.Range(0, 7),
                                ],
                            ),
                        }
                    )
                ),
            }
        ),
        VIRTUAL_ROUTER_TYPE: properties.Schema(
            properties.Schema.STRING,
            _('VIRTUAL_ROUTER_TYPE.'),
            update_allowed=True,
            required=False,
        ),
        ANNOTATIONS: properties.Schema(
            properties.Schema.MAP,
            _('ANNOTATIONS.'),
            update_allowed=True,
            required=False,
            schema={
                ANNOTATIONS_KEY_VALUE_PAIR: properties.Schema(
                    properties.Schema.LIST,
                    _('ANNOTATIONS_KEY_VALUE_PAIR.'),
                    update_allowed=True,
                    required=False,
                    schema=properties.Schema(
                        properties.Schema.MAP,
                        schema={
                            ANNOTATIONS_KEY_VALUE_PAIR_KEY: properties.Schema(
                                properties.Schema.STRING,
                                _('ANNOTATIONS_KEY_VALUE_PAIR_KEY.'),
                                update_allowed=True,
                                required=False,
                            ),
                            ANNOTATIONS_KEY_VALUE_PAIR_VALUE: properties.Schema(
                                properties.Schema.STRING,
                                _('ANNOTATIONS_KEY_VALUE_PAIR_VALUE.'),
                                update_allowed=True,
                                required=False,
                            ),
                        }
                    )
                ),
            }
        ),
        VIRTUAL_MACHINE_REFS: properties.Schema(
            properties.Schema.LIST,
            _('VIRTUAL_MACHINE_REFS.'),
            update_allowed=True,
            required=False,
        ),
        NETWORK_IPAM_REFS: properties.Schema(
            properties.Schema.LIST,
            _('NETWORK_IPAM_REFS.'),
            update_allowed=True,
            required=False,
        ),
        NETWORK_IPAM_REFS_DATA: properties.Schema(
            properties.Schema.LIST,
            _('NETWORK_IPAM_REFS_DATA.'),
            update_allowed=True,
            required=False,
            schema=properties.Schema(
                properties.Schema.MAP,
                schema={
                    NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS: properties.Schema(
                        properties.Schema.LIST,
                        _('NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS.'),
                        update_allowed=True,
                        required=False,
                        schema=properties.Schema(
                            properties.Schema.MAP,
                            schema={
                                NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_START: properties.Schema(
                                    properties.Schema.STRING,
                                    _('NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_START.'),
                                    update_allowed=True,
                                    required=False,
                                ),
                                NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_END: properties.Schema(
                                    properties.Schema.STRING,
                                    _('NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_END.'),
                                    update_allowed=True,
                                    required=False,
                                ),
                                NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_VROUTER_SPECIFIC_POOL: properties.Schema(
                                    properties.Schema.BOOLEAN,
                                    _('NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_VROUTER_SPECIFIC_POOL.'),
                                    update_allowed=True,
                                    required=False,
                                ),
                            }
                        )
                    ),
                    NETWORK_IPAM_REFS_DATA_SUBNET: properties.Schema(
                        properties.Schema.LIST,
                        _('NETWORK_IPAM_REFS_DATA_SUBNET.'),
                        update_allowed=True,
                        required=False,
                        schema=properties.Schema(
                            properties.Schema.MAP,
                            schema={
                                NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX: properties.Schema(
                                    properties.Schema.STRING,
                                    _('NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX.'),
                                    update_allowed=True,
                                    required=False,
                                ),
                                NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX_LEN: properties.Schema(
                                    properties.Schema.INTEGER,
                                    _('NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX_LEN.'),
                                    update_allowed=True,
                                    required=False,
                                ),
                            }
                        )
                    ),
                }
            )
        ),
        SUB_CLUSTER_REFS: properties.Schema(
            properties.Schema.LIST,
            _('SUB_CLUSTER_REFS.'),
            update_allowed=True,
            required=False,
        ),
        TAG_REFS: properties.Schema(
            properties.Schema.LIST,
            _('TAG_REFS.'),
            update_allowed=True,
            required=False,
        ),
        GLOBAL_SYSTEM_CONFIG: properties.Schema(
            properties.Schema.STRING,
            _('GLOBAL_SYSTEM_CONFIG.'),
            update_allowed=True,
            required=False,
        ),
    }

    attributes_schema = {
        NAME: attributes.Schema(
            _('NAME.'),
        ),
        FQ_NAME: attributes.Schema(
            _('FQ_NAME.'),
        ),
        DISPLAY_NAME: attributes.Schema(
            _('DISPLAY_NAME.'),
        ),
        VIRTUAL_ROUTER_IP_ADDRESS: attributes.Schema(
            _('VIRTUAL_ROUTER_IP_ADDRESS.'),
        ),
        VIRTUAL_ROUTER_DPDK_ENABLED: attributes.Schema(
            _('VIRTUAL_ROUTER_DPDK_ENABLED.'),
        ),
        PERMS2: attributes.Schema(
            _('PERMS2.'),
        ),
        VIRTUAL_ROUTER_TYPE: attributes.Schema(
            _('VIRTUAL_ROUTER_TYPE.'),
        ),
        ANNOTATIONS: attributes.Schema(
            _('ANNOTATIONS.'),
        ),
        VIRTUAL_MACHINE_REFS: attributes.Schema(
            _('VIRTUAL_MACHINE_REFS.'),
        ),
        NETWORK_IPAM_REFS: attributes.Schema(
            _('NETWORK_IPAM_REFS.'),
        ),
        NETWORK_IPAM_REFS_DATA: attributes.Schema(
            _('NETWORK_IPAM_REFS_DATA.'),
        ),
        SUB_CLUSTER_REFS: attributes.Schema(
            _('SUB_CLUSTER_REFS.'),
        ),
        TAG_REFS: attributes.Schema(
            _('TAG_REFS.'),
        ),
        GLOBAL_SYSTEM_CONFIG: attributes.Schema(
            _('GLOBAL_SYSTEM_CONFIG.'),
        ),
    }

    update_allowed_keys = ('Properties',)

    @contrail.set_auth_token
    def handle_create(self):
        parent_obj = None
        if parent_obj is None and self.properties.get(self.GLOBAL_SYSTEM_CONFIG) and self.properties.get(self.GLOBAL_SYSTEM_CONFIG) != 'config-root':
            try:
                parent_obj = self.vnc_lib().global_system_config_read(fq_name_str=self.properties.get(self.GLOBAL_SYSTEM_CONFIG))
            except vnc_api.NoIdError:
                parent_obj = self.vnc_lib().global_system_config_read(id=str(uuid.UUID(self.properties.get(self.GLOBAL_SYSTEM_CONFIG))))
            except:
                parent_obj = None

        if parent_obj is None and self.properties.get(self.GLOBAL_SYSTEM_CONFIG) != 'config-root':
            raise Exception('Error: parent is not specified in template!')

        obj_0 = vnc_api.VirtualRouter(name=self.properties[self.NAME],
            parent_obj=parent_obj)

        if self.properties.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(self.properties.get(self.DISPLAY_NAME))
        if self.properties.get(self.VIRTUAL_ROUTER_IP_ADDRESS) is not None:
            obj_0.set_virtual_router_ip_address(self.properties.get(self.VIRTUAL_ROUTER_IP_ADDRESS))
        if self.properties.get(self.VIRTUAL_ROUTER_DPDK_ENABLED) is not None:
            obj_0.set_virtual_router_dpdk_enabled(self.properties.get(self.VIRTUAL_ROUTER_DPDK_ENABLED))
        if self.properties.get(self.PERMS2) is not None:
            obj_1 = vnc_api.PermType2()
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER) is not None:
                obj_1.set_owner(self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER))
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER_ACCESS) is not None:
                obj_1.set_owner_access(self.properties.get(self.PERMS2, {}).get(self.PERMS2_OWNER_ACCESS))
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_GLOBAL_ACCESS) is not None:
                obj_1.set_global_access(self.properties.get(self.PERMS2, {}).get(self.PERMS2_GLOBAL_ACCESS))
            if self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE) is not None:
                for index_1 in range(len(self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE))):
                    obj_2 = vnc_api.ShareType()
                    if self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT) is not None:
                        obj_2.set_tenant(self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT))
                    if self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT_ACCESS) is not None:
                        obj_2.set_tenant_access(self.properties.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT_ACCESS))
                    obj_1.add_share(obj_2)
            obj_0.set_perms2(obj_1)
        if self.properties.get(self.VIRTUAL_ROUTER_TYPE) is not None:
            obj_0.set_virtual_router_type(self.properties.get(self.VIRTUAL_ROUTER_TYPE))
        if self.properties.get(self.ANNOTATIONS) is not None:
            obj_1 = vnc_api.KeyValuePairs()
            if self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR) is not None:
                for index_1 in range(len(self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR))):
                    obj_2 = vnc_api.KeyValuePair()
                    if self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY) is not None:
                        obj_2.set_key(self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY))
                    if self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE) is not None:
                        obj_2.set_value(self.properties.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE))
                    obj_1.add_key_value_pair(obj_2)
            obj_0.set_annotations(obj_1)

        # reference to virtual_machine_refs
        if self.properties.get(self.VIRTUAL_MACHINE_REFS):
            for index_0 in range(len(self.properties.get(self.VIRTUAL_MACHINE_REFS))):
                try:
                    ref_obj = self.vnc_lib().virtual_machine_read(
                        id=self.properties.get(self.VIRTUAL_MACHINE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().virtual_machine_read(
                        fq_name_str=self.properties.get(self.VIRTUAL_MACHINE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_virtual_machine(ref_obj)

        # reference to network_ipam_refs
        if len(self.properties.get(self.NETWORK_IPAM_REFS) or []) != len(self.properties.get(self.NETWORK_IPAM_REFS_DATA) or []):
            raise Exception(_('virtual-router: specify network_ipam_refs for each network_ipam_refs_data.'))
        obj_1 = None
        if self.properties.get(self.NETWORK_IPAM_REFS_DATA) is not None:
            for index_0 in range(len(self.properties.get(self.NETWORK_IPAM_REFS_DATA))):
                obj_1 = vnc_api.VirtualRouterNetworkIpamType()
                if self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS) is not None:
                    for index_1 in range(len(self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS))):
                        obj_2 = vnc_api.AllocationPoolType()
                        if self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_START) is not None:
                            obj_2.set_start(self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_START))
                        if self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_END) is not None:
                            obj_2.set_end(self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_END))
                        if self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_VROUTER_SPECIFIC_POOL) is not None:
                            obj_2.set_vrouter_specific_pool(self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_VROUTER_SPECIFIC_POOL))
                        obj_1.add_allocation_pools(obj_2)
                if self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET) is not None:
                    for index_1 in range(len(self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET))):
                        obj_2 = vnc_api.SubnetType()
                        if self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX) is not None:
                            obj_2.set_ip_prefix(self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX))
                        if self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX_LEN) is not None:
                            obj_2.set_ip_prefix_len(self.properties.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX_LEN))
                        obj_1.add_subnet(obj_2)

                if self.properties.get(self.NETWORK_IPAM_REFS):
                    try:
                        ref_obj = self.vnc_lib().network_ipam_read(
                            id=self.properties.get(self.NETWORK_IPAM_REFS)[index_0]
                        )
                    except vnc_api.NoIdError:
                        ref_obj = self.vnc_lib().network_ipam_read(
                            fq_name_str=self.properties.get(self.NETWORK_IPAM_REFS)[index_0]
                        )
                    except Exception as e:
                        raise Exception(_('%s') % str(e))
                    obj_0.add_network_ipam(ref_obj, obj_1)

        # reference to sub_cluster_refs
        if self.properties.get(self.SUB_CLUSTER_REFS):
            for index_0 in range(len(self.properties.get(self.SUB_CLUSTER_REFS))):
                try:
                    ref_obj = self.vnc_lib().sub_cluster_read(
                        id=self.properties.get(self.SUB_CLUSTER_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().sub_cluster_read(
                        fq_name_str=self.properties.get(self.SUB_CLUSTER_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_sub_cluster(ref_obj)

        # reference to tag_refs
        if self.properties.get(self.TAG_REFS):
            for index_0 in range(len(self.properties.get(self.TAG_REFS))):
                try:
                    ref_obj = self.vnc_lib().tag_read(
                        id=self.properties.get(self.TAG_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().tag_read(
                        fq_name_str=self.properties.get(self.TAG_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_tag(ref_obj)

        try:
            obj_uuid = super(ContrailVirtualRouter, self).resource_create(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

        self.resource_id_set(obj_uuid)

    @contrail.set_auth_token
    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        try:
            obj_0 = self.vnc_lib().virtual_router_read(
                id=self.resource_id
            )
        except Exception as e:
            raise Exception(_('%s') % str(e))

        if prop_diff.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(prop_diff.get(self.DISPLAY_NAME))
        if prop_diff.get(self.VIRTUAL_ROUTER_IP_ADDRESS) is not None:
            obj_0.set_virtual_router_ip_address(prop_diff.get(self.VIRTUAL_ROUTER_IP_ADDRESS))
        if prop_diff.get(self.VIRTUAL_ROUTER_DPDK_ENABLED) is not None:
            obj_0.set_virtual_router_dpdk_enabled(prop_diff.get(self.VIRTUAL_ROUTER_DPDK_ENABLED))
        if prop_diff.get(self.PERMS2) is not None:
            obj_1 = vnc_api.PermType2()
            if prop_diff.get(self.PERMS2, {}).get(self.PERMS2_OWNER) is not None:
                obj_1.set_owner(prop_diff.get(self.PERMS2, {}).get(self.PERMS2_OWNER))
            if prop_diff.get(self.PERMS2, {}).get(self.PERMS2_OWNER_ACCESS) is not None:
                obj_1.set_owner_access(prop_diff.get(self.PERMS2, {}).get(self.PERMS2_OWNER_ACCESS))
            if prop_diff.get(self.PERMS2, {}).get(self.PERMS2_GLOBAL_ACCESS) is not None:
                obj_1.set_global_access(prop_diff.get(self.PERMS2, {}).get(self.PERMS2_GLOBAL_ACCESS))
            if prop_diff.get(self.PERMS2, {}).get(self.PERMS2_SHARE) is not None:
                for index_1 in range(len(prop_diff.get(self.PERMS2, {}).get(self.PERMS2_SHARE))):
                    obj_2 = vnc_api.ShareType()
                    if prop_diff.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT) is not None:
                        obj_2.set_tenant(prop_diff.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT))
                    if prop_diff.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT_ACCESS) is not None:
                        obj_2.set_tenant_access(prop_diff.get(self.PERMS2, {}).get(self.PERMS2_SHARE, {})[index_1].get(self.PERMS2_SHARE_TENANT_ACCESS))
                    obj_1.add_share(obj_2)
            obj_0.set_perms2(obj_1)
        if prop_diff.get(self.VIRTUAL_ROUTER_TYPE) is not None:
            obj_0.set_virtual_router_type(prop_diff.get(self.VIRTUAL_ROUTER_TYPE))
        if prop_diff.get(self.ANNOTATIONS) is not None:
            obj_1 = vnc_api.KeyValuePairs()
            if prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR) is not None:
                for index_1 in range(len(prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR))):
                    obj_2 = vnc_api.KeyValuePair()
                    if prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY) is not None:
                        obj_2.set_key(prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_KEY))
                    if prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE) is not None:
                        obj_2.set_value(prop_diff.get(self.ANNOTATIONS, {}).get(self.ANNOTATIONS_KEY_VALUE_PAIR, {})[index_1].get(self.ANNOTATIONS_KEY_VALUE_PAIR_VALUE))
                    obj_1.add_key_value_pair(obj_2)
            obj_0.set_annotations(obj_1)

        # reference to virtual_machine_refs
        ref_obj_list = []
        if self.VIRTUAL_MACHINE_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.VIRTUAL_MACHINE_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().virtual_machine_read(
                        id=prop_diff.get(self.VIRTUAL_MACHINE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().virtual_machine_read(
                        fq_name_str=prop_diff.get(self.VIRTUAL_MACHINE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_virtual_machine_list(ref_obj_list)
            # End: reference to virtual_machine_refs

        # reference to network_ipam
        update = 0
        if not self.NETWORK_IPAM_REFS in prop_diff:
            ref_obj_list = [ref['to'] for ref in obj_0.get_network_ipam_refs() or []]
        else:
            ref_obj_list = []
            update = 1
        if not self.NETWORK_IPAM_REFS_DATA in prop_diff:
            ref_data_list = [ref['attr'] for ref in obj_0.get_network_ipam_refs() or []]
        else:
            ref_data_list = []

        if prop_diff.get(self.NETWORK_IPAM_REFS_DATA) is not None:
            for index_0 in range(len(prop_diff.get(self.NETWORK_IPAM_REFS_DATA))):
                obj_1 = vnc_api.VirtualRouterNetworkIpamType()
                if prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS) is not None:
                    for index_1 in range(len(prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS))):
                        obj_2 = vnc_api.AllocationPoolType()
                        if prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_START) is not None:
                            obj_2.set_start(prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_START))
                        if prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_END) is not None:
                            obj_2.set_end(prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_END))
                        if prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_VROUTER_SPECIFIC_POOL) is not None:
                            obj_2.set_vrouter_specific_pool(prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_ALLOCATION_POOLS_VROUTER_SPECIFIC_POOL))
                        obj_1.add_allocation_pools(obj_2)
                if prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET) is not None:
                    for index_1 in range(len(prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET))):
                        obj_2 = vnc_api.SubnetType()
                        if prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX) is not None:
                            obj_2.set_ip_prefix(prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX))
                        if prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX_LEN) is not None:
                            obj_2.set_ip_prefix_len(prop_diff.get(self.NETWORK_IPAM_REFS_DATA, {})[index_0].get(self.NETWORK_IPAM_REFS_DATA_SUBNET, {})[index_1].get(self.NETWORK_IPAM_REFS_DATA_SUBNET_IP_PREFIX_LEN))
                        obj_1.add_subnet(obj_2)
                ref_data_list.append(obj_1)
        if self.NETWORK_IPAM_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.NETWORK_IPAM_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().network_ipam_read(
                        id=prop_diff.get(self.NETWORK_IPAM_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().network_ipam_read(
                        fq_name_str=prop_diff.get(self.NETWORK_IPAM_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append(ref_obj.fq_name)

        if len(ref_obj_list) != len(ref_data_list):
            raise Exception(_('virtual-router: specify network_ipam_refs_data for each network_ipam_refs.'))

        if update or ref_obj_list or ref_data_list:
            obj_0.set_network_ipam_list(ref_obj_list, ref_data_list)
        # End: reference to network_ipam_refs

        # reference to sub_cluster_refs
        ref_obj_list = []
        if self.SUB_CLUSTER_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.SUB_CLUSTER_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().sub_cluster_read(
                        id=prop_diff.get(self.SUB_CLUSTER_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().sub_cluster_read(
                        fq_name_str=prop_diff.get(self.SUB_CLUSTER_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_sub_cluster_list(ref_obj_list)
            # End: reference to sub_cluster_refs

        # reference to tag_refs
        ref_obj_list = []
        if self.TAG_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.TAG_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().tag_read(
                        id=prop_diff.get(self.TAG_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().tag_read(
                        fq_name_str=prop_diff.get(self.TAG_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_tag_list(ref_obj_list)
            # End: reference to tag_refs

        try:
            self.vnc_lib().virtual_router_update(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

    @contrail.set_auth_token
    def handle_delete(self):
        if self.resource_id is None:
            return

        try:
            self.vnc_lib().virtual_router_delete(id=self.resource_id)
        except Exception as ex:
            self._ignore_not_found(ex)
            LOG.warn(_('virtual_router %s already deleted.') % self.name)

    @contrail.set_auth_token
    def _show_resource(self):
        obj = self.vnc_lib().virtual_router_read(id=self.resource_id)
        obj_dict = obj.serialize_to_json()
        return obj_dict


def resource_mapping():
    return {
        'OS::ContrailV2::VirtualRouter': ContrailVirtualRouter,
    }
