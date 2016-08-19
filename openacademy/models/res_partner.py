# -*- coding: utf-8 -*-
# © 2016, Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    instructor = fields.Boolean()
    session_ids = fields.Many2many(
        'openacademy.session', string="Attended Sessions", readonly=True)
