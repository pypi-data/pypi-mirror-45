
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


class ContrailStructuredSyslogApplicationRecord(contrail.ContrailResource):
    PROPERTIES = (
        NAME, FQ_NAME, STRUCTURED_SYSLOG_APP_CATEGORY, DISPLAY_NAME, STRUCTURED_SYSLOG_APP_SERVICE_TAGS, PERMS2, PERMS2_OWNER, PERMS2_OWNER_ACCESS, PERMS2_GLOBAL_ACCESS, PERMS2_SHARE, PERMS2_SHARE_TENANT, PERMS2_SHARE_TENANT_ACCESS, STRUCTURED_SYSLOG_APP_RISK, STRUCTURED_SYSLOG_APP_SUBCATEGORY, STRUCTURED_SYSLOG_APP_GROUPS, ANNOTATIONS, ANNOTATIONS_KEY_VALUE_PAIR, ANNOTATIONS_KEY_VALUE_PAIR_KEY, ANNOTATIONS_KEY_VALUE_PAIR_VALUE, TAG_REFS, STRUCTURED_SYSLOG_CONFIG
    ) = (
        'name', 'fq_name', 'structured_syslog_app_category', 'display_name', 'structured_syslog_app_service_tags', 'perms2', 'perms2_owner', 'perms2_owner_access', 'perms2_global_access', 'perms2_share', 'perms2_share_tenant', 'perms2_share_tenant_access', 'structured_syslog_app_risk', 'structured_syslog_app_subcategory', 'structured_syslog_app_groups', 'annotations', 'annotations_key_value_pair', 'annotations_key_value_pair_key', 'annotations_key_value_pair_value', 'tag_refs', 'structured_syslog_config'
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
        STRUCTURED_SYSLOG_APP_CATEGORY: properties.Schema(
            properties.Schema.STRING,
            _('STRUCTURED_SYSLOG_APP_CATEGORY.'),
            update_allowed=True,
            required=False,
        ),
        DISPLAY_NAME: properties.Schema(
            properties.Schema.STRING,
            _('DISPLAY_NAME.'),
            update_allowed=True,
            required=False,
        ),
        STRUCTURED_SYSLOG_APP_SERVICE_TAGS: properties.Schema(
            properties.Schema.STRING,
            _('STRUCTURED_SYSLOG_APP_SERVICE_TAGS.'),
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
        STRUCTURED_SYSLOG_APP_RISK: properties.Schema(
            properties.Schema.STRING,
            _('STRUCTURED_SYSLOG_APP_RISK.'),
            update_allowed=True,
            required=False,
        ),
        STRUCTURED_SYSLOG_APP_SUBCATEGORY: properties.Schema(
            properties.Schema.STRING,
            _('STRUCTURED_SYSLOG_APP_SUBCATEGORY.'),
            update_allowed=True,
            required=False,
        ),
        STRUCTURED_SYSLOG_APP_GROUPS: properties.Schema(
            properties.Schema.STRING,
            _('STRUCTURED_SYSLOG_APP_GROUPS.'),
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
        TAG_REFS: properties.Schema(
            properties.Schema.LIST,
            _('TAG_REFS.'),
            update_allowed=True,
            required=False,
        ),
        STRUCTURED_SYSLOG_CONFIG: properties.Schema(
            properties.Schema.STRING,
            _('STRUCTURED_SYSLOG_CONFIG.'),
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
        STRUCTURED_SYSLOG_APP_CATEGORY: attributes.Schema(
            _('STRUCTURED_SYSLOG_APP_CATEGORY.'),
        ),
        DISPLAY_NAME: attributes.Schema(
            _('DISPLAY_NAME.'),
        ),
        STRUCTURED_SYSLOG_APP_SERVICE_TAGS: attributes.Schema(
            _('STRUCTURED_SYSLOG_APP_SERVICE_TAGS.'),
        ),
        PERMS2: attributes.Schema(
            _('PERMS2.'),
        ),
        STRUCTURED_SYSLOG_APP_RISK: attributes.Schema(
            _('STRUCTURED_SYSLOG_APP_RISK.'),
        ),
        STRUCTURED_SYSLOG_APP_SUBCATEGORY: attributes.Schema(
            _('STRUCTURED_SYSLOG_APP_SUBCATEGORY.'),
        ),
        STRUCTURED_SYSLOG_APP_GROUPS: attributes.Schema(
            _('STRUCTURED_SYSLOG_APP_GROUPS.'),
        ),
        ANNOTATIONS: attributes.Schema(
            _('ANNOTATIONS.'),
        ),
        TAG_REFS: attributes.Schema(
            _('TAG_REFS.'),
        ),
        STRUCTURED_SYSLOG_CONFIG: attributes.Schema(
            _('STRUCTURED_SYSLOG_CONFIG.'),
        ),
    }

    update_allowed_keys = ('Properties',)

    @contrail.set_auth_token
    def handle_create(self):
        parent_obj = None
        if parent_obj is None and self.properties.get(self.STRUCTURED_SYSLOG_CONFIG) and self.properties.get(self.STRUCTURED_SYSLOG_CONFIG) != 'config-root':
            try:
                parent_obj = self.vnc_lib().structured_syslog_config_read(fq_name_str=self.properties.get(self.STRUCTURED_SYSLOG_CONFIG))
            except vnc_api.NoIdError:
                parent_obj = self.vnc_lib().structured_syslog_config_read(id=str(uuid.UUID(self.properties.get(self.STRUCTURED_SYSLOG_CONFIG))))
            except:
                parent_obj = None

        if parent_obj is None and self.properties.get(self.STRUCTURED_SYSLOG_CONFIG) != 'config-root':
            raise Exception('Error: parent is not specified in template!')

        obj_0 = vnc_api.StructuredSyslogApplicationRecord(name=self.properties[self.NAME],
            parent_obj=parent_obj)

        if self.properties.get(self.STRUCTURED_SYSLOG_APP_CATEGORY) is not None:
            obj_0.set_structured_syslog_app_category(self.properties.get(self.STRUCTURED_SYSLOG_APP_CATEGORY))
        if self.properties.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(self.properties.get(self.DISPLAY_NAME))
        if self.properties.get(self.STRUCTURED_SYSLOG_APP_SERVICE_TAGS) is not None:
            obj_0.set_structured_syslog_app_service_tags(self.properties.get(self.STRUCTURED_SYSLOG_APP_SERVICE_TAGS))
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
        if self.properties.get(self.STRUCTURED_SYSLOG_APP_RISK) is not None:
            obj_0.set_structured_syslog_app_risk(self.properties.get(self.STRUCTURED_SYSLOG_APP_RISK))
        if self.properties.get(self.STRUCTURED_SYSLOG_APP_SUBCATEGORY) is not None:
            obj_0.set_structured_syslog_app_subcategory(self.properties.get(self.STRUCTURED_SYSLOG_APP_SUBCATEGORY))
        if self.properties.get(self.STRUCTURED_SYSLOG_APP_GROUPS) is not None:
            obj_0.set_structured_syslog_app_groups(self.properties.get(self.STRUCTURED_SYSLOG_APP_GROUPS))
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
            obj_uuid = super(ContrailStructuredSyslogApplicationRecord, self).resource_create(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

        self.resource_id_set(obj_uuid)

    @contrail.set_auth_token
    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        try:
            obj_0 = self.vnc_lib().structured_syslog_application_record_read(
                id=self.resource_id
            )
        except Exception as e:
            raise Exception(_('%s') % str(e))

        if prop_diff.get(self.STRUCTURED_SYSLOG_APP_CATEGORY) is not None:
            obj_0.set_structured_syslog_app_category(prop_diff.get(self.STRUCTURED_SYSLOG_APP_CATEGORY))
        if prop_diff.get(self.DISPLAY_NAME) is not None:
            obj_0.set_display_name(prop_diff.get(self.DISPLAY_NAME))
        if prop_diff.get(self.STRUCTURED_SYSLOG_APP_SERVICE_TAGS) is not None:
            obj_0.set_structured_syslog_app_service_tags(prop_diff.get(self.STRUCTURED_SYSLOG_APP_SERVICE_TAGS))
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
        if prop_diff.get(self.STRUCTURED_SYSLOG_APP_RISK) is not None:
            obj_0.set_structured_syslog_app_risk(prop_diff.get(self.STRUCTURED_SYSLOG_APP_RISK))
        if prop_diff.get(self.STRUCTURED_SYSLOG_APP_SUBCATEGORY) is not None:
            obj_0.set_structured_syslog_app_subcategory(prop_diff.get(self.STRUCTURED_SYSLOG_APP_SUBCATEGORY))
        if prop_diff.get(self.STRUCTURED_SYSLOG_APP_GROUPS) is not None:
            obj_0.set_structured_syslog_app_groups(prop_diff.get(self.STRUCTURED_SYSLOG_APP_GROUPS))
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
            self.vnc_lib().structured_syslog_application_record_update(obj_0)
        except Exception as e:
            raise Exception(_('%s') % str(e))

    @contrail.set_auth_token
    def handle_delete(self):
        if self.resource_id is None:
            return

        try:
            self.vnc_lib().structured_syslog_application_record_delete(id=self.resource_id)
        except Exception as ex:
            self._ignore_not_found(ex)
            LOG.warn(_('structured_syslog_application_record %s already deleted.') % self.name)

    @contrail.set_auth_token
    def _show_resource(self):
        obj = self.vnc_lib().structured_syslog_application_record_read(id=self.resource_id)
        obj_dict = obj.serialize_to_json()
        return obj_dict


def resource_mapping():
    return {
        'OS::ContrailV2::StructuredSyslogApplicationRecord': ContrailStructuredSyslogApplicationRecord,
    }
