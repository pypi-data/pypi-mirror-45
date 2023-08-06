
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


class ContrailCard(contrail.ContrailResource):
    PROPERTIES = (
        NAME, FQ_NAME, INTERFACE_MAP, INTERFACE_MAP_PORT_INFO, INTERFACE_MAP_PORT_INFO_NAME, INTERFACE_MAP_PORT_INFO_TYPE_, INTERFACE_MAP_PORT_INFO_PORT_SPEED, INTERFACE_MAP_PORT_INFO_CHANNELIZED, INTERFACE_MAP_PORT_INFO_CHANNELIZED_PORT_SPEED, INTERFACE_MAP_PORT_INFO_PORT_GROUP, INTERFACE_MAP_PORT_INFO_LABELS, DISPLAY_NAME, PERMS2, PERMS2_OWNER, PERMS2_OWNER_ACCESS, PERMS2_GLOBAL_ACCESS, PERMS2_SHARE, PERMS2_SHARE_TENANT, PERMS2_SHARE_TENANT_ACCESS, ANNOTATIONS, ANNOTATIONS_KEY_VALUE_PAIR, ANNOTATIONS_KEY_VALUE_PAIR_KEY, ANNOTATIONS_KEY_VALUE_PAIR_VALUE, TAG_REFS
    ) = (
        'name', 'fq_name', 'interface_map', 'interface_map_port_info', 'interface_map_port_info_name', 'interface_map_port_info_type_', 'interface_map_port_info_port_speed', 'interface_map_port_info_channelized', 'interface_map_port_info_channelized_port_speed', 'interface_map_port_info_port_group', 'interface_map_port_info_labels', 'display_name', 'perms2', 'perms2_owner', 'perms2_owner_access', 'perms2_global_access', 'perms2_share', 'perms2_share_tenant', 'perms2_share_tenant_access', 'annotations', 'annotations_key_value_pair', 'annotations_key_value_pair_key', 'annotations_key_value_pair_value', 'tag_refs'
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
        INTERFACE_MAP: properties.Schema(
            properties.Schema.MAP,
            _('INTERFACE_MAP.'),
            update_allowed=True,
            required=False,
            schema={
                INTERFACE_MAP_PORT_INFO: properties.Schema(
                    properties.Schema.LIST,
                    _('INTERFACE_MAP_PORT_INFO.'),
                    update_allowed=True,
                    required=False,
                    schema=properties.Schema(
                        properties.Schema.MAP,
                        schema={
                            INTERFACE_MAP_PORT_INFO_NAME: properties.Schema(
                                properties.Schema.STRING,
                                _('INTERFACE_MAP_PORT_INFO_NAME.'),
                                update_allowed=True,
                                required=False,
                            ),
                            INTERFACE_MAP_PORT_INFO_TYPE_: properties.Schema(
                                properties.Schema.STRING,
                                _('INTERFACE_MAP_PORT_INFO_TYPE_.'),
                                update_allowed=True,
                                required=False,
                                constraints=[
                                    constraints.AllowedValues([u'fc', u'ge', u'xe', u'xle', u'et', u'fte', u'me', u'em']),
                                ],
                            ),
                            INTERFACE_MAP_PORT_INFO_PORT_SPEED: properties.Schema(
                                properties.Schema.STRING,
                                _('INTERFACE_MAP_PORT_INFO_PORT_SPEED.'),
                                update_allowed=True,
                                required=False,
                                constraints=[
                                    constraints.AllowedValues([u'1G', u'10G', u'40G', u'100G']),
                                ],
                            ),
                            INTERFACE_MAP_PORT_INFO_CHANNELIZED: properties.Schema(
                                properties.Schema.BOOLEAN,
                                _('INTERFACE_MAP_PORT_INFO_CHANNELIZED.'),
                                update_allowed=True,
                                required=False,
                            ),
                            INTERFACE_MAP_PORT_INFO_CHANNELIZED_PORT_SPEED: properties.Schema(
                                properties.Schema.STRING,
                                _('INTERFACE_MAP_PORT_INFO_CHANNELIZED_PORT_SPEED.'),
                                update_allowed=True,
                                required=False,
                                constraints=[
                                    constraints.AllowedValues([u'1G', u'10G', u'40G', u'100G']),
                                ],
                            ),
                            INTERFACE_MAP_PORT_INFO_PORT_GROUP: properties.Schema(
                                properties.Schema.STRING,
                                _('INTERFACE_MAP_PORT_INFO_PORT_GROUP.'),
                                update_allowed=True,
                                required=False,
                            ),
                            INTERFACE_MAP_PORT_INFO_LABELS: properties.Schema(
                                properties.Schema.LIST,
                                _('INTERFACE_MAP_PORT_INFO_LABELS.'),
                                update_allowed=True,
                                required=False,
                            ),
                        }
                    )
                ),
            }
        ),
        DISPLAY_NAME: properties.Schema(
            properties.Schema.STRING,
            _('DISPLAY_NAME.'),
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
        TAG_REFS: properties.Schema(
            properties.Schema.LIST,
            _('TAG_REFS.'),
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
        INTERFACE_MAP: attributes.Schema(
            _('INTERFACE_MAP.'),
        ),
        DISPLAY_NAME: attributes.Schema(
            _('DISPLAY_NAME.'),
        ),
        PERMS2: attributes.Schema(
            _('PERMS2.'),
        ),
        ANNOTATIONS: attributes.Schema(
            _('ANNOTATIONS.'),
        ),
        TAG_REFS: attributes.Schema(
            _('TAG_REFS.'),
        ),
    }

    update_allowed_keys = ('Properties',)

    @contrail.set_auth_token
    def handle_create(self):
        obj_0 = vnc_api.Card(name=self.properties[self.NAME])

        if self.properties.get(self.INTERFACE_MAP) is not None:
            obj_1 = vnc_api.InterfaceMapType()
            if self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO) is not None:
                for index_1 in range(len(self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO))):
                    obj_2 = vnc_api.PortInfoType()
                    if self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_NAME) is not None:
                        obj_2.set_name(self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_NAME))
                    if self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_TYPE_) is not None:
                        obj_2.set_type_(self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_TYPE_))
                    if self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_PORT_SPEED) is not None:
                        obj_2.set_port_speed(self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_PORT_SPEED))
                    if self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_CHANNELIZED) is not None:
                        obj_2.set_channelized(self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_CHANNELIZED))
                    if self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_CHANNELIZED_PORT_SPEED) is not None:
                        obj_2.set_channelized_port_speed(self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_CHANNELIZED_PORT_SPEED))
                    if self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_PORT_GROUP) is not None:
                        obj_2.set_port_group(self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_PORT_GROUP))
                    if self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_LABELS) is not None:
                        for index_2 in range(len(self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_LABELS))):
                            obj_2.add_labels(self.properties.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_LABELS)[index_2])
                    obj_1.add_port_info(obj_2)
            obj_0.set_interface_map(obj_1)
        if self.properties.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(self.properties.get(self.DISPLAY_NAME))
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
            obj_uuid = super(ContrailCard, self).resource_create(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

        self.resource_id_set(obj_uuid)

    @contrail.set_auth_token
    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        try:
            obj_0 = self.vnc_lib().card_read(
                id=self.resource_id
            )
        except Exception as e:
            raise Exception(_('%s') % str(e))

        if prop_diff.get(self.INTERFACE_MAP) is not None:
            obj_1 = vnc_api.InterfaceMapType()
            if prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO) is not None:
                for index_1 in range(len(prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO))):
                    obj_2 = vnc_api.PortInfoType()
                    if prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_NAME) is not None:
                        obj_2.set_name(prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_NAME))
                    if prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_TYPE_) is not None:
                        obj_2.set_type_(prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_TYPE_))
                    if prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_PORT_SPEED) is not None:
                        obj_2.set_port_speed(prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_PORT_SPEED))
                    if prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_CHANNELIZED) is not None:
                        obj_2.set_channelized(prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_CHANNELIZED))
                    if prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_CHANNELIZED_PORT_SPEED) is not None:
                        obj_2.set_channelized_port_speed(prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_CHANNELIZED_PORT_SPEED))
                    if prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_PORT_GROUP) is not None:
                        obj_2.set_port_group(prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_PORT_GROUP))
                    if prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_LABELS) is not None:
                        for index_2 in range(len(prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_LABELS))):
                            obj_2.add_labels(prop_diff.get(self.INTERFACE_MAP, {}).get(self.INTERFACE_MAP_PORT_INFO, {})[index_1].get(self.INTERFACE_MAP_PORT_INFO_LABELS)[index_2])
                    obj_1.add_port_info(obj_2)
            obj_0.set_interface_map(obj_1)
        if prop_diff.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(prop_diff.get(self.DISPLAY_NAME))
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
            self.vnc_lib().card_update(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

    @contrail.set_auth_token
    def handle_delete(self):
        if self.resource_id is None:
            return

        try:
            self.vnc_lib().card_delete(id=self.resource_id)
        except Exception as ex:
            self._ignore_not_found(ex)
            LOG.warn(_('card %s already deleted.') % self.name)

    @contrail.set_auth_token
    def _show_resource(self):
        obj = self.vnc_lib().card_read(id=self.resource_id)
        obj_dict = obj.serialize_to_json()
        return obj_dict


def resource_mapping():
    return {
        'OS::ContrailV2::Card': ContrailCard,
    }
