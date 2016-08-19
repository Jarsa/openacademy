# -*- coding: utf-8 -*-
# © 2016, Jarsa Sistemas, S.A. de C.V.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Openacademy",
    "summary": "This module is to demostrate how to develop a module in Odoo",
    "version": "9.0.1.0.0",
    "category": "Development",
    "website": "https://www.jarsa.com.mx",
    "author": "Jarsa Sistemas",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "mail",
    ],
    "data": [
        'views/openacademy.xml',
        'views/openacademy_course.xml',
        'views/openacademy_session.xml',
        'views/res_partner_view.xml',
        'views/openacademy_session_workflow.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizards/openacademy_wizard.xml',
        'report/openacademy_session.xml',
    ],
    "demo": [
        "demo/openacademy_course.xml",
    ],
}
