import logging

from odoo import SUPERUSER_ID, api, models

_logger = logging.getLogger(__name__)


class MixinErpUserForbiddenFields(models.AbstractModel):
    _name = "mixin.erp.user.forbidden.fields"
    _description = "Mixin ERP User Forbidden Fields"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._remove_erp_user_system_forbidden_fields(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._remove_erp_user_system_forbidden_fields(vals)
        return super().write(vals)

    @api.model
    def _get_erp_user_system_forbidden_fields(self):
        return []

    @api.model
    def _is_current_user_only_erp_user(self):
        return self.env.user._is_user_only_erp_user()

    def _is_user_only_erp_user(self):
        self.ensure_one()
        if self.id == SUPERUSER_ID:
            return False
        return self.has_group(
            "base_group_erp_user.group_erp_user"
        ) and not self.has_group("base.group_erp_manager")

    @api.model
    def _remove_erp_user_system_forbidden_fields(self, values):
        if not self._is_current_user_only_erp_user():
            return
        for fname in self._get_erp_user_system_forbidden_fields():
            values.pop(fname, False)
