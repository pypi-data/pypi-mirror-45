
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


class ContrailLogicalRouter(contrail.ContrailResource):
    PROPERTIES = (
        NAME, FQ_NAME, DISPLAY_NAME, CONFIGURED_ROUTE_TARGET_LIST, CONFIGURED_ROUTE_TARGET_LIST_ROUTE_TARGET, PERMS2, PERMS2_OWNER, PERMS2_OWNER_ACCESS, PERMS2_GLOBAL_ACCESS, PERMS2_SHARE, PERMS2_SHARE_TENANT, PERMS2_SHARE_TENANT_ACCESS, ANNOTATIONS, ANNOTATIONS_KEY_VALUE_PAIR, ANNOTATIONS_KEY_VALUE_PAIR_KEY, ANNOTATIONS_KEY_VALUE_PAIR_VALUE, VXLAN_NETWORK_IDENTIFIER, LOGICAL_ROUTER_TYPE, LOGICAL_ROUTER_GATEWAY_EXTERNAL, VIRTUAL_MACHINE_INTERFACE_REFS, VIRTUAL_NETWORK_REFS, VIRTUAL_NETWORK_REFS_DATA, VIRTUAL_NETWORK_REFS_DATA_LOGICAL_ROUTER_VIRTUAL_NETWORK_TYPE, TAG_REFS, ROUTE_TABLE_REFS, ROUTE_TARGET_REFS, BGPVPN_REFS, PHYSICAL_ROUTER_REFS, SERVICE_INSTANCE_REFS, PROJECT
    ) = (
        'name', 'fq_name', 'display_name', 'configured_route_target_list', 'configured_route_target_list_route_target', 'perms2', 'perms2_owner', 'perms2_owner_access', 'perms2_global_access', 'perms2_share', 'perms2_share_tenant', 'perms2_share_tenant_access', 'annotations', 'annotations_key_value_pair', 'annotations_key_value_pair_key', 'annotations_key_value_pair_value', 'vxlan_network_identifier', 'logical_router_type', 'logical_router_gateway_external', 'virtual_machine_interface_refs', 'virtual_network_refs', 'virtual_network_refs_data', 'virtual_network_refs_data_logical_router_virtual_network_type', 'tag_refs', 'route_table_refs', 'route_target_refs', 'bgpvpn_refs', 'physical_router_refs', 'service_instance_refs', 'project'
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
        CONFIGURED_ROUTE_TARGET_LIST: properties.Schema(
            properties.Schema.MAP,
            _('CONFIGURED_ROUTE_TARGET_LIST.'),
            update_allowed=True,
            required=False,
            schema={
                CONFIGURED_ROUTE_TARGET_LIST_ROUTE_TARGET: properties.Schema(
                    properties.Schema.LIST,
                    _('CONFIGURED_ROUTE_TARGET_LIST_ROUTE_TARGET.'),
                    update_allowed=True,
                    required=False,
                ),
            }
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
        VXLAN_NETWORK_IDENTIFIER: properties.Schema(
            properties.Schema.STRING,
            _('VXLAN_NETWORK_IDENTIFIER.'),
            update_allowed=True,
            required=False,
        ),
        LOGICAL_ROUTER_TYPE: properties.Schema(
            properties.Schema.STRING,
            _('LOGICAL_ROUTER_TYPE.'),
            update_allowed=True,
            required=False,
        ),
        LOGICAL_ROUTER_GATEWAY_EXTERNAL: properties.Schema(
            properties.Schema.BOOLEAN,
            _('LOGICAL_ROUTER_GATEWAY_EXTERNAL.'),
            update_allowed=True,
            required=False,
        ),
        VIRTUAL_MACHINE_INTERFACE_REFS: properties.Schema(
            properties.Schema.LIST,
            _('VIRTUAL_MACHINE_INTERFACE_REFS.'),
            update_allowed=True,
            required=False,
        ),
        VIRTUAL_NETWORK_REFS: properties.Schema(
            properties.Schema.LIST,
            _('VIRTUAL_NETWORK_REFS.'),
            update_allowed=True,
            required=False,
        ),
        VIRTUAL_NETWORK_REFS_DATA: properties.Schema(
            properties.Schema.LIST,
            _('VIRTUAL_NETWORK_REFS_DATA.'),
            update_allowed=True,
            required=False,
            schema=properties.Schema(
                properties.Schema.MAP,
                schema={
                    VIRTUAL_NETWORK_REFS_DATA_LOGICAL_ROUTER_VIRTUAL_NETWORK_TYPE: properties.Schema(
                        properties.Schema.STRING,
                        _('VIRTUAL_NETWORK_REFS_DATA_LOGICAL_ROUTER_VIRTUAL_NETWORK_TYPE.'),
                        update_allowed=True,
                        required=False,
                        constraints=[
                            constraints.AllowedValues([u'ExternalGateway', u'InternalVirtualNetwork']),
                        ],
                    ),
                }
            )
        ),
        TAG_REFS: properties.Schema(
            properties.Schema.LIST,
            _('TAG_REFS.'),
            update_allowed=True,
            required=False,
        ),
        ROUTE_TABLE_REFS: properties.Schema(
            properties.Schema.LIST,
            _('ROUTE_TABLE_REFS.'),
            update_allowed=True,
            required=False,
        ),
        ROUTE_TARGET_REFS: properties.Schema(
            properties.Schema.LIST,
            _('ROUTE_TARGET_REFS.'),
            update_allowed=True,
            required=False,
        ),
        BGPVPN_REFS: properties.Schema(
            properties.Schema.LIST,
            _('BGPVPN_REFS.'),
            update_allowed=True,
            required=False,
        ),
        PHYSICAL_ROUTER_REFS: properties.Schema(
            properties.Schema.LIST,
            _('PHYSICAL_ROUTER_REFS.'),
            update_allowed=True,
            required=False,
        ),
        SERVICE_INSTANCE_REFS: properties.Schema(
            properties.Schema.LIST,
            _('SERVICE_INSTANCE_REFS.'),
            update_allowed=True,
            required=False,
        ),
        PROJECT: properties.Schema(
            properties.Schema.STRING,
            _('PROJECT.'),
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
        CONFIGURED_ROUTE_TARGET_LIST: attributes.Schema(
            _('CONFIGURED_ROUTE_TARGET_LIST.'),
        ),
        PERMS2: attributes.Schema(
            _('PERMS2.'),
        ),
        ANNOTATIONS: attributes.Schema(
            _('ANNOTATIONS.'),
        ),
        VXLAN_NETWORK_IDENTIFIER: attributes.Schema(
            _('VXLAN_NETWORK_IDENTIFIER.'),
        ),
        LOGICAL_ROUTER_TYPE: attributes.Schema(
            _('LOGICAL_ROUTER_TYPE.'),
        ),
        LOGICAL_ROUTER_GATEWAY_EXTERNAL: attributes.Schema(
            _('LOGICAL_ROUTER_GATEWAY_EXTERNAL.'),
        ),
        VIRTUAL_MACHINE_INTERFACE_REFS: attributes.Schema(
            _('VIRTUAL_MACHINE_INTERFACE_REFS.'),
        ),
        VIRTUAL_NETWORK_REFS: attributes.Schema(
            _('VIRTUAL_NETWORK_REFS.'),
        ),
        VIRTUAL_NETWORK_REFS_DATA: attributes.Schema(
            _('VIRTUAL_NETWORK_REFS_DATA.'),
        ),
        TAG_REFS: attributes.Schema(
            _('TAG_REFS.'),
        ),
        ROUTE_TABLE_REFS: attributes.Schema(
            _('ROUTE_TABLE_REFS.'),
        ),
        ROUTE_TARGET_REFS: attributes.Schema(
            _('ROUTE_TARGET_REFS.'),
        ),
        BGPVPN_REFS: attributes.Schema(
            _('BGPVPN_REFS.'),
        ),
        PHYSICAL_ROUTER_REFS: attributes.Schema(
            _('PHYSICAL_ROUTER_REFS.'),
        ),
        SERVICE_INSTANCE_REFS: attributes.Schema(
            _('SERVICE_INSTANCE_REFS.'),
        ),
        PROJECT: attributes.Schema(
            _('PROJECT.'),
        ),
    }

    update_allowed_keys = ('Properties',)

    @contrail.set_auth_token
    def handle_create(self):
        parent_obj = None
        if parent_obj is None and self.properties.get(self.PROJECT) and self.properties.get(self.PROJECT) != 'config-root':
            try:
                parent_obj = self.vnc_lib().project_read(fq_name_str=self.properties.get(self.PROJECT))
            except vnc_api.NoIdError:
                parent_obj = self.vnc_lib().project_read(id=str(uuid.UUID(self.properties.get(self.PROJECT))))
            except:
                parent_obj = None

        if parent_obj is None and self.properties.get(self.PROJECT) != 'config-root':
            tenant_id = self.stack.context.tenant_id
            parent_obj = self.vnc_lib().project_read(id=str(uuid.UUID(tenant_id)))

        if parent_obj is None and self.properties.get(self.PROJECT) != 'config-root':
            raise Exception('Error: parent is not specified in template!')

        obj_0 = vnc_api.LogicalRouter(name=self.properties[self.NAME],
            parent_obj=parent_obj)

        if self.properties.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(self.properties.get(self.DISPLAY_NAME))
        if self.properties.get(self.CONFIGURED_ROUTE_TARGET_LIST) is not None:
            obj_1 = vnc_api.RouteTargetList()
            if self.properties.get(self.CONFIGURED_ROUTE_TARGET_LIST, {}).get(self.CONFIGURED_ROUTE_TARGET_LIST_ROUTE_TARGET) is not None:
                for index_1 in range(len(self.properties.get(self.CONFIGURED_ROUTE_TARGET_LIST, {}).get(self.CONFIGURED_ROUTE_TARGET_LIST_ROUTE_TARGET))):
                    obj_1.add_route_target(self.properties.get(self.CONFIGURED_ROUTE_TARGET_LIST, {}).get(self.CONFIGURED_ROUTE_TARGET_LIST_ROUTE_TARGET)[index_1])
            obj_0.set_configured_route_target_list(obj_1)
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
        if self.properties.get(self.VXLAN_NETWORK_IDENTIFIER) is not None:
            obj_0.set_vxlan_network_identifier(self.properties.get(self.VXLAN_NETWORK_IDENTIFIER))
        if self.properties.get(self.LOGICAL_ROUTER_TYPE) is not None:
            obj_0.set_logical_router_type(self.properties.get(self.LOGICAL_ROUTER_TYPE))
        if self.properties.get(self.LOGICAL_ROUTER_GATEWAY_EXTERNAL) is not None:
            obj_0.set_logical_router_gateway_external(self.properties.get(self.LOGICAL_ROUTER_GATEWAY_EXTERNAL))

        # reference to virtual_machine_interface_refs
        if self.properties.get(self.VIRTUAL_MACHINE_INTERFACE_REFS):
            for index_0 in range(len(self.properties.get(self.VIRTUAL_MACHINE_INTERFACE_REFS))):
                try:
                    ref_obj = self.vnc_lib().virtual_machine_interface_read(
                        id=self.properties.get(self.VIRTUAL_MACHINE_INTERFACE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().virtual_machine_interface_read(
                        fq_name_str=self.properties.get(self.VIRTUAL_MACHINE_INTERFACE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_virtual_machine_interface(ref_obj)

        # reference to virtual_network_refs
        if len(self.properties.get(self.VIRTUAL_NETWORK_REFS) or []) != len(self.properties.get(self.VIRTUAL_NETWORK_REFS_DATA) or []):
            raise Exception(_('logical-router: specify virtual_network_refs for each virtual_network_refs_data.'))
        obj_1 = None
        if self.properties.get(self.VIRTUAL_NETWORK_REFS_DATA) is not None:
            for index_0 in range(len(self.properties.get(self.VIRTUAL_NETWORK_REFS_DATA))):
                obj_1 = vnc_api.LogicalRouterVirtualNetworkType()
                if self.properties.get(self.VIRTUAL_NETWORK_REFS_DATA, {})[index_0].get(self.VIRTUAL_NETWORK_REFS_DATA_LOGICAL_ROUTER_VIRTUAL_NETWORK_TYPE) is not None:
                    obj_1.set_logical_router_virtual_network_type(self.properties.get(self.VIRTUAL_NETWORK_REFS_DATA, {})[index_0].get(self.VIRTUAL_NETWORK_REFS_DATA_LOGICAL_ROUTER_VIRTUAL_NETWORK_TYPE))

                if self.properties.get(self.VIRTUAL_NETWORK_REFS):
                    try:
                        ref_obj = self.vnc_lib().virtual_network_read(
                            id=self.properties.get(self.VIRTUAL_NETWORK_REFS)[index_0]
                        )
                    except vnc_api.NoIdError:
                        ref_obj = self.vnc_lib().virtual_network_read(
                            fq_name_str=self.properties.get(self.VIRTUAL_NETWORK_REFS)[index_0]
                        )
                    except Exception as e:
                        raise Exception(_('%s') % str(e))
                    obj_0.add_virtual_network(ref_obj, obj_1)

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

        # reference to route_table_refs
        if self.properties.get(self.ROUTE_TABLE_REFS):
            for index_0 in range(len(self.properties.get(self.ROUTE_TABLE_REFS))):
                try:
                    ref_obj = self.vnc_lib().route_table_read(
                        id=self.properties.get(self.ROUTE_TABLE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().route_table_read(
                        fq_name_str=self.properties.get(self.ROUTE_TABLE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_route_table(ref_obj)

        # reference to route_target_refs
        if self.properties.get(self.ROUTE_TARGET_REFS):
            for index_0 in range(len(self.properties.get(self.ROUTE_TARGET_REFS))):
                try:
                    ref_obj = self.vnc_lib().route_target_read(
                        id=self.properties.get(self.ROUTE_TARGET_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().route_target_read(
                        fq_name_str=self.properties.get(self.ROUTE_TARGET_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_route_target(ref_obj)

        # reference to bgpvpn_refs
        if self.properties.get(self.BGPVPN_REFS):
            for index_0 in range(len(self.properties.get(self.BGPVPN_REFS))):
                try:
                    ref_obj = self.vnc_lib().bgpvpn_read(
                        id=self.properties.get(self.BGPVPN_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().bgpvpn_read(
                        fq_name_str=self.properties.get(self.BGPVPN_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_bgpvpn(ref_obj)

        # reference to physical_router_refs
        if self.properties.get(self.PHYSICAL_ROUTER_REFS):
            for index_0 in range(len(self.properties.get(self.PHYSICAL_ROUTER_REFS))):
                try:
                    ref_obj = self.vnc_lib().physical_router_read(
                        id=self.properties.get(self.PHYSICAL_ROUTER_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().physical_router_read(
                        fq_name_str=self.properties.get(self.PHYSICAL_ROUTER_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_physical_router(ref_obj)

        # reference to service_instance_refs
        if self.properties.get(self.SERVICE_INSTANCE_REFS):
            for index_0 in range(len(self.properties.get(self.SERVICE_INSTANCE_REFS))):
                try:
                    ref_obj = self.vnc_lib().service_instance_read(
                        id=self.properties.get(self.SERVICE_INSTANCE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().service_instance_read(
                        fq_name_str=self.properties.get(self.SERVICE_INSTANCE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_service_instance(ref_obj)

        try:
            obj_uuid = super(ContrailLogicalRouter, self).resource_create(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

        self.resource_id_set(obj_uuid)

    @contrail.set_auth_token
    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        try:
            obj_0 = self.vnc_lib().logical_router_read(
                id=self.resource_id
            )
        except Exception as e:
            raise Exception(_('%s') % str(e))

        if prop_diff.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(prop_diff.get(self.DISPLAY_NAME))
        if prop_diff.get(self.CONFIGURED_ROUTE_TARGET_LIST) is not None:
            obj_1 = vnc_api.RouteTargetList()
            if prop_diff.get(self.CONFIGURED_ROUTE_TARGET_LIST, {}).get(self.CONFIGURED_ROUTE_TARGET_LIST_ROUTE_TARGET) is not None:
                for index_1 in range(len(prop_diff.get(self.CONFIGURED_ROUTE_TARGET_LIST, {}).get(self.CONFIGURED_ROUTE_TARGET_LIST_ROUTE_TARGET))):
                    obj_1.add_route_target(prop_diff.get(self.CONFIGURED_ROUTE_TARGET_LIST, {}).get(self.CONFIGURED_ROUTE_TARGET_LIST_ROUTE_TARGET)[index_1])
            obj_0.set_configured_route_target_list(obj_1)
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
        if prop_diff.get(self.VXLAN_NETWORK_IDENTIFIER) is not None:
            obj_0.set_vxlan_network_identifier(prop_diff.get(self.VXLAN_NETWORK_IDENTIFIER))
        if prop_diff.get(self.LOGICAL_ROUTER_TYPE) is not None:
            obj_0.set_logical_router_type(prop_diff.get(self.LOGICAL_ROUTER_TYPE))
        if prop_diff.get(self.LOGICAL_ROUTER_GATEWAY_EXTERNAL) is not None:
            obj_0.set_logical_router_gateway_external(prop_diff.get(self.LOGICAL_ROUTER_GATEWAY_EXTERNAL))

        # reference to virtual_machine_interface_refs
        ref_obj_list = []
        if self.VIRTUAL_MACHINE_INTERFACE_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.VIRTUAL_MACHINE_INTERFACE_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().virtual_machine_interface_read(
                        id=prop_diff.get(self.VIRTUAL_MACHINE_INTERFACE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().virtual_machine_interface_read(
                        fq_name_str=prop_diff.get(self.VIRTUAL_MACHINE_INTERFACE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_virtual_machine_interface_list(ref_obj_list)
            # End: reference to virtual_machine_interface_refs

        # reference to virtual_network
        update = 0
        if not self.VIRTUAL_NETWORK_REFS in prop_diff:
            ref_obj_list = [ref['to'] for ref in obj_0.get_virtual_network_refs() or []]
        else:
            ref_obj_list = []
            update = 1
        if not self.VIRTUAL_NETWORK_REFS_DATA in prop_diff:
            ref_data_list = [ref['attr'] for ref in obj_0.get_virtual_network_refs() or []]
        else:
            ref_data_list = []

        if prop_diff.get(self.VIRTUAL_NETWORK_REFS_DATA) is not None:
            for index_0 in range(len(prop_diff.get(self.VIRTUAL_NETWORK_REFS_DATA))):
                obj_1 = vnc_api.LogicalRouterVirtualNetworkType()
                if prop_diff.get(self.VIRTUAL_NETWORK_REFS_DATA, {})[index_0].get(self.VIRTUAL_NETWORK_REFS_DATA_LOGICAL_ROUTER_VIRTUAL_NETWORK_TYPE) is not None:
                    obj_1.set_logical_router_virtual_network_type(prop_diff.get(self.VIRTUAL_NETWORK_REFS_DATA, {})[index_0].get(self.VIRTUAL_NETWORK_REFS_DATA_LOGICAL_ROUTER_VIRTUAL_NETWORK_TYPE))
                ref_data_list.append(obj_1)
        if self.VIRTUAL_NETWORK_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.VIRTUAL_NETWORK_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().virtual_network_read(
                        id=prop_diff.get(self.VIRTUAL_NETWORK_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().virtual_network_read(
                        fq_name_str=prop_diff.get(self.VIRTUAL_NETWORK_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append(ref_obj.fq_name)

        if len(ref_obj_list) != len(ref_data_list):
            raise Exception(_('logical-router: specify virtual_network_refs_data for each virtual_network_refs.'))

        if update or ref_obj_list or ref_data_list:
            obj_0.set_virtual_network_list(ref_obj_list, ref_data_list)
        # End: reference to virtual_network_refs

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

        # reference to route_table_refs
        ref_obj_list = []
        if self.ROUTE_TABLE_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.ROUTE_TABLE_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().route_table_read(
                        id=prop_diff.get(self.ROUTE_TABLE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().route_table_read(
                        fq_name_str=prop_diff.get(self.ROUTE_TABLE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_route_table_list(ref_obj_list)
            # End: reference to route_table_refs

        # reference to route_target_refs
        ref_obj_list = []
        if self.ROUTE_TARGET_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.ROUTE_TARGET_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().route_target_read(
                        id=prop_diff.get(self.ROUTE_TARGET_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().route_target_read(
                        fq_name_str=prop_diff.get(self.ROUTE_TARGET_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_route_target_list(ref_obj_list)
            # End: reference to route_target_refs

        # reference to bgpvpn_refs
        ref_obj_list = []
        if self.BGPVPN_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.BGPVPN_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().bgpvpn_read(
                        id=prop_diff.get(self.BGPVPN_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().bgpvpn_read(
                        fq_name_str=prop_diff.get(self.BGPVPN_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_bgpvpn_list(ref_obj_list)
            # End: reference to bgpvpn_refs

        # reference to physical_router_refs
        ref_obj_list = []
        if self.PHYSICAL_ROUTER_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.PHYSICAL_ROUTER_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().physical_router_read(
                        id=prop_diff.get(self.PHYSICAL_ROUTER_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().physical_router_read(
                        fq_name_str=prop_diff.get(self.PHYSICAL_ROUTER_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_physical_router_list(ref_obj_list)
            # End: reference to physical_router_refs

        # reference to service_instance_refs
        ref_obj_list = []
        if self.SERVICE_INSTANCE_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.SERVICE_INSTANCE_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().service_instance_read(
                        id=prop_diff.get(self.SERVICE_INSTANCE_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().service_instance_read(
                        fq_name_str=prop_diff.get(self.SERVICE_INSTANCE_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_service_instance_list(ref_obj_list)
            # End: reference to service_instance_refs

        try:
            self.vnc_lib().logical_router_update(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

    @contrail.set_auth_token
    def handle_delete(self):
        if self.resource_id is None:
            return

        try:
            self.vnc_lib().logical_router_delete(id=self.resource_id)
        except Exception as ex:
            self._ignore_not_found(ex)
            LOG.warn(_('logical_router %s already deleted.') % self.name)

    @contrail.set_auth_token
    def _show_resource(self):
        obj = self.vnc_lib().logical_router_read(id=self.resource_id)
        obj_dict = obj.serialize_to_json()
        return obj_dict


def resource_mapping():
    return {
        'OS::ContrailV2::LogicalRouter': ContrailLogicalRouter,
    }
