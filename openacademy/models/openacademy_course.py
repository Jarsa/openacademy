# -*- coding: utf-8 -*-
# © 2016, Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class OpenacademyCourse(models.Model):
    _name = 'openacademy.course'
    _description = 'Course'
    _inherit = 'mail.thread'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(
        'res.users', ondelete='set null', string='Responsible',
        default=lambda self: self.env.user)
    session_ids = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         _("The title of the course should not be the description")),

        ('name_unique',
         'UNIQUE(name)',
         _("The course title must be unique")),
        ]

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(OpenacademyCourse, self).copy(default)
