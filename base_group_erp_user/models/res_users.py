# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = ["res.users", "mixin.erp.user.forbidden.fields"]

    @api.model
    def _get_erp_user_system_forbidden_fields(self):
        return [
            "groups_id",
        ]

    @api.model
    def _default_groups(self):
        if self._is_current_user_only_erp_user():
            return []
        return super()._default_groups()
