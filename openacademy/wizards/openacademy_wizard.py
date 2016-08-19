# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ClassName(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = 'Openacademy Wizard'

    def _default_session_ids(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many(
        'openacademy.session',
        string="Sessions", required=True, default=_default_session_ids)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    @api.multi
    def subscribe(self):
        import ipdb; ipdb.set_trace()
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}
