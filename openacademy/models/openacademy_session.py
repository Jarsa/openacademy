# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class OpenacademySession(models.Model):
    _name = 'openacademy.session'
    _description = 'Sessions'
    _inherit = 'mail.thread'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one(
        'res.partner', string="Instructor",
        domain=['|', ('instructor', '=', True),
                ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one(
        'openacademy.course', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Atendees")
    taken_seats = fields.Float(compute='_compute_taken_seats')
    active = fields.Boolean(default=True)
    end_date = fields.Date(
        compute='_compute_end_date', inverse='_inverse_end_date')
    hours = fields.Float(string="Duration in hours",
                         compute='_compute_hours', inverse='_inverse_hours')
    attendees_count = fields.Integer(
        string="Attendees count",
        compute='_compute_attendees_count',
        store=True)
    color = fields.Integer()
    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ], default='draft')

    @api.depends('seats', 'attendee_ids')
    def _compute_taken_seats(self):
        for rec in self:
            if not rec.seats:
                rec.taken_seats = 0.0
            else:
                rec.taken_seats = (
                    100.0 * len(rec.attendee_ids) / rec.seats)

    @api.onchange('seats', 'attendee_ids')
    def _onchange_verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of available seats may not be "
                                 "negative"),
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                },
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for rec in self:
            if rec.instructor_id in rec.attendee_ids:
                raise ValidationError(
                    _("A session's instructor can't be an attendee"))

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.duration):
                rec.end_date = rec.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            start = fields.Datetime.from_string(rec.start_date)
            duration = timedelta(days=rec.duration, seconds=-1)
            rec.end_date = start + duration

    def _inverse_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.end_date):
                continue

            # Compute the difference between dates,but:Friday-Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(rec.start_date)
            end_date = fields.Datetime.from_string(rec.end_date)
            rec.duration = (end_date - start_date).days + 1

    @api.depends('duration')
    def _compute_hours(self):
        for rec in self:
            rec.hours = rec.duration * 24

    def _inverse_hours(self):
        for rec in self:
            rec.duration = rec.hours / 24

    @api.depends('attendee_ids')
    def _compute_attendees_count(self):
        for rec in self:
            rec.attendees_count = len(rec.attendee_ids)

    @api.multi
    def action_draft(self):
        self.state = 'draft'
        self.message_post('Set to Draft')

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'
        self.message_post('Set to Confirmed')

    @api.multi
    def action_done(self):
        self.state = 'done'
        self.message_post('Set to Done')
