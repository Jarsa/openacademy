# -*- coding: utf-8 -*-
# © 2016 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from psycopg2 import IntegrityError
from openerp.tests.common import TransactionCase
from openerp.tools import mute_logger


class TestGlobalOpenacademyCourse(TransactionCase):
    """
    This will test model openacademy.course
    """

# Global variables
    def setUp(self):
        """
        Define global variables
        """
        super(TestGlobalOpenacademyCourse, self).setUp()
        self.course = self.env['openacademy.course']

# Global methods

    def create_course(self, name_test, description_test):
        self.course.create({
            'name': name_test,
            'description': description_test,
            })

    @mute_logger('openerp.sql_db')
    def test_10_course_same_name_description(self):
        '''
        This test check that you cannot make a course with the same name and
        description
        '''
        with self.assertRaisesRegexp(
            IntegrityError,
            'new row for relation "openacademy_course" violates check '
                'constraint "openacademy_course_name_description_check"'):
            self.create_course('test', 'test')

    def test_30_duplicate_course(self):
        course = self.env.ref('openacademy.course_00')
        course.copy()
