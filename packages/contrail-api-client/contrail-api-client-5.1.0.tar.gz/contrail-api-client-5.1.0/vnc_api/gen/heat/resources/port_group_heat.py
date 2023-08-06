
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


class ContrailPortGroup(contrail.ContrailResource):
    PROPERTIES = (
        NAME, FQ_NAME, DISPLAY_NAME, BMS_PORT_GROUP_INFO, BMS_PORT_GROUP_INFO_STANDALONE_PORTS_SUPPORTED, BMS_PORT_GROUP_INFO_NODE_UUID, BMS_PORT_GROUP_INFO_PROPERTIES, BMS_PORT_GROUP_INFO_PROPERTIES_MIIMON, BMS_PORT_GROUP_INFO_PROPERTIES_XMIT_HASH_POLICY, BMS_PORT_GROUP_INFO_ADDRESS, BMS_PORT_GROUP_INFO_MODE, ANNOTATIONS, ANNOTATIONS_KEY_VALUE_PAIR, ANNOTATIONS_KEY_VALUE_PAIR_KEY, ANNOTATIONS_KEY_VALUE_PAIR_VALUE, PERMS2, PERMS2_OWNER, PERMS2_OWNER_ACCESS, PERMS2_GLOBAL_ACCESS, PERMS2_SHARE, PERMS2_SHARE_TENANT, PERMS2_SHARE_TENANT_ACCESS, TAG_REFS, PORT_REFS, NODE
    ) = (
        'name', 'fq_name', 'display_name', 'bms_port_group_info', 'bms_port_group_info_standalone_ports_supported', 'bms_port_group_info_node_uuid', 'bms_port_group_info_properties', 'bms_port_group_info_properties_miimon', 'bms_port_group_info_properties_xmit_hash_policy', 'bms_port_group_info_address', 'bms_port_group_info_mode', 'annotations', 'annotations_key_value_pair', 'annotations_key_value_pair_key', 'annotations_key_value_pair_value', 'perms2', 'perms2_owner', 'perms2_owner_access', 'perms2_global_access', 'perms2_share', 'perms2_share_tenant', 'perms2_share_tenant_access', 'tag_refs', 'port_refs', 'node'
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
        BMS_PORT_GROUP_INFO: properties.Schema(
            properties.Schema.MAP,
            _('BMS_PORT_GROUP_INFO.'),
            update_allowed=True,
            required=False,
            schema={
                BMS_PORT_GROUP_INFO_STANDALONE_PORTS_SUPPORTED: properties.Schema(
                    properties.Schema.BOOLEAN,
                    _('BMS_PORT_GROUP_INFO_STANDALONE_PORTS_SUPPORTED.'),
                    update_allowed=True,
                    required=False,
                ),
                BMS_PORT_GROUP_INFO_NODE_UUID: properties.Schema(
                    properties.Schema.STRING,
                    _('BMS_PORT_GROUP_INFO_NODE_UUID.'),
                    update_allowed=True,
                    required=False,
                ),
                BMS_PORT_GROUP_INFO_PROPERTIES: properties.Schema(
                    properties.Schema.MAP,
                    _('BMS_PORT_GROUP_INFO_PROPERTIES.'),
                    update_allowed=True,
                    required=False,
                    schema={
                        BMS_PORT_GROUP_INFO_PROPERTIES_MIIMON: properties.Schema(
                            properties.Schema.INTEGER,
                            _('BMS_PORT_GROUP_INFO_PROPERTIES_MIIMON.'),
                            update_allowed=True,
                            required=False,
                        ),
                        BMS_PORT_GROUP_INFO_PROPERTIES_XMIT_HASH_POLICY: properties.Schema(
                            properties.Schema.STRING,
                            _('BMS_PORT_GROUP_INFO_PROPERTIES_XMIT_HASH_POLICY.'),
                            update_allowed=True,
                            required=False,
                        ),
                    }
                ),
                BMS_PORT_GROUP_INFO_ADDRESS: properties.Schema(
                    properties.Schema.STRING,
                    _('BMS_PORT_GROUP_INFO_ADDRESS.'),
                    update_allowed=True,
                    required=False,
                ),
                BMS_PORT_GROUP_INFO_MODE: properties.Schema(
                    properties.Schema.STRING,
                    _('BMS_PORT_GROUP_INFO_MODE.'),
                    update_allowed=True,
                    required=False,
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
        TAG_REFS: properties.Schema(
            properties.Schema.LIST,
            _('TAG_REFS.'),
            update_allowed=True,
            required=False,
        ),
        PORT_REFS: properties.Schema(
            properties.Schema.LIST,
            _('PORT_REFS.'),
            update_allowed=True,
            required=False,
        ),
        NODE: properties.Schema(
            properties.Schema.STRING,
            _('NODE.'),
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
        BMS_PORT_GROUP_INFO: attributes.Schema(
            _('BMS_PORT_GROUP_INFO.'),
        ),
        ANNOTATIONS: attributes.Schema(
            _('ANNOTATIONS.'),
        ),
        PERMS2: attributes.Schema(
            _('PERMS2.'),
        ),
        TAG_REFS: attributes.Schema(
            _('TAG_REFS.'),
        ),
        PORT_REFS: attributes.Schema(
            _('PORT_REFS.'),
        ),
        NODE: attributes.Schema(
            _('NODE.'),
        ),
    }

    update_allowed_keys = ('Properties',)

    @contrail.set_auth_token
    def handle_create(self):
        parent_obj = None
        if parent_obj is None and self.properties.get(self.NODE) and self.properties.get(self.NODE) != 'config-root':
            try:
                parent_obj = self.vnc_lib().node_read(fq_name_str=self.properties.get(self.NODE))
            except vnc_api.NoIdError:
                parent_obj = self.vnc_lib().node_read(id=str(uuid.UUID(self.properties.get(self.NODE))))
            except:
                parent_obj = None

        if parent_obj is None and self.properties.get(self.NODE) != 'config-root':
            raise Exception('Error: parent is not specified in template!')

        obj_0 = vnc_api.PortGroup(name=self.properties[self.NAME],
            parent_obj=parent_obj)

        if self.properties.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(self.properties.get(self.DISPLAY_NAME))
        if self.properties.get(self.BMS_PORT_GROUP_INFO) is not None:
            obj_1 = vnc_api.BaremetalPortGroupInfo()
            if self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_STANDALONE_PORTS_SUPPORTED) is not None:
                obj_1.set_standalone_ports_supported(self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_STANDALONE_PORTS_SUPPORTED))
            if self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_NODE_UUID) is not None:
                obj_1.set_node_uuid(self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_NODE_UUID))
            if self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES) is not None:
                obj_2 = vnc_api.PortGroupProperties()
                if self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES_MIIMON) is not None:
                    obj_2.set_miimon(self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES_MIIMON))
                if self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES_XMIT_HASH_POLICY) is not None:
                    obj_2.set_xmit_hash_policy(self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES_XMIT_HASH_POLICY))
                obj_1.set_properties(obj_2)
            if self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_ADDRESS) is not None:
                obj_1.set_address(self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_ADDRESS))
            if self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_MODE) is not None:
                obj_1.set_mode(self.properties.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_MODE))
            obj_0.set_bms_port_group_info(obj_1)
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

        # reference to port_refs
        if self.properties.get(self.PORT_REFS):
            for index_0 in range(len(self.properties.get(self.PORT_REFS))):
                try:
                    ref_obj = self.vnc_lib().port_read(
                        id=self.properties.get(self.PORT_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().port_read(
                        fq_name_str=self.properties.get(self.PORT_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                obj_0.add_port(ref_obj)

        try:
            obj_uuid = super(ContrailPortGroup, self).resource_create(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

        self.resource_id_set(obj_uuid)

    @contrail.set_auth_token
    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        try:
            obj_0 = self.vnc_lib().port_group_read(
                id=self.resource_id
            )
        except Exception as e:
            raise Exception(_('%s') % str(e))

        if prop_diff.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(prop_diff.get(self.DISPLAY_NAME))
        if prop_diff.get(self.BMS_PORT_GROUP_INFO) is not None:
            obj_1 = vnc_api.BaremetalPortGroupInfo()
            if prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_STANDALONE_PORTS_SUPPORTED) is not None:
                obj_1.set_standalone_ports_supported(prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_STANDALONE_PORTS_SUPPORTED))
            if prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_NODE_UUID) is not None:
                obj_1.set_node_uuid(prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_NODE_UUID))
            if prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES) is not None:
                obj_2 = vnc_api.PortGroupProperties()
                if prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES_MIIMON) is not None:
                    obj_2.set_miimon(prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES_MIIMON))
                if prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES_XMIT_HASH_POLICY) is not None:
                    obj_2.set_xmit_hash_policy(prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES, {}).get(self.BMS_PORT_GROUP_INFO_PROPERTIES_XMIT_HASH_POLICY))
                obj_1.set_properties(obj_2)
            if prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_ADDRESS) is not None:
                obj_1.set_address(prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_ADDRESS))
            if prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_MODE) is not None:
                obj_1.set_mode(prop_diff.get(self.BMS_PORT_GROUP_INFO, {}).get(self.BMS_PORT_GROUP_INFO_MODE))
            obj_0.set_bms_port_group_info(obj_1)
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

        # reference to port_refs
        ref_obj_list = []
        if self.PORT_REFS in prop_diff:
            for index_0 in range(len(prop_diff.get(self.PORT_REFS) or [])):
                try:
                    ref_obj = self.vnc_lib().port_read(
                        id=prop_diff.get(self.PORT_REFS)[index_0]
                    )
                except vnc_api.NoIdError:
                    ref_obj = self.vnc_lib().port_read(
                        fq_name_str=prop_diff.get(self.PORT_REFS)[index_0]
                    )
                except Exception as e:
                    raise Exception(_('%s') % str(e))
                ref_obj_list.append({'to':ref_obj.fq_name})

            obj_0.set_port_list(ref_obj_list)
            # End: reference to port_refs

        try:
            self.vnc_lib().port_group_update(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

    @contrail.set_auth_token
    def handle_delete(self):
        if self.resource_id is None:
            return

        try:
            self.vnc_lib().port_group_delete(id=self.resource_id)
        except Exception as ex:
            self._ignore_not_found(ex)
            LOG.warn(_('port_group %s already deleted.') % self.name)

    @contrail.set_auth_token
    def _show_resource(self):
        obj = self.vnc_lib().port_group_read(id=self.resource_id)
        obj_dict = obj.serialize_to_json()
        return obj_dict


def resource_mapping():
    return {
        'OS::ContrailV2::PortGroup': ContrailPortGroup,
    }
