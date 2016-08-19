# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class OpenacademySessionReport(models.AbstractModel):
    _name = 'report.openacademy.report_session_view'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'openacademy.report_session_view')
        self.env.cr.execute(
            'SELECT * FROM res_partner WHERE is_company IS True')
        partners = self.env.cr.dictfetchall()
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'partners': partners
        }
        return report_obj.render('openacademy.report_session_view', docargs)
