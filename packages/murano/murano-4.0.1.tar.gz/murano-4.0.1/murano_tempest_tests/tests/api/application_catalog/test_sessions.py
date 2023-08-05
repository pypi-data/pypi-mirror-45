#    Copyright (c) 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.lib import decorators

from murano_tempest_tests.tests.api.application_catalog import base
from murano_tempest_tests import utils


class TestSessions(base.BaseApplicationCatalogTest):

    @classmethod
    def resource_setup(cls):
        super(TestSessions, cls).resource_setup()
        name = utils.generate_name(cls.__name__)
        cls.environment = cls.application_catalog_client.\
            create_environment(name)

    @classmethod
    def resource_cleanup(cls):
        cls.application_catalog_client.\
            delete_environment(cls.environment['id'])
        super(TestSessions, cls).resource_cleanup()

    @decorators.attr(type='smoke')
    @decorators.idempotent_id('9f8ca4dd-1159-4c12-bd97-84ee7f36775e')
    def test_create_session(self):
        session = self.application_catalog_client.\
            create_session(self.environment['id'])
        self.addCleanup(self.application_catalog_client.delete_session,
                        self.environment['id'], session['id'])
        self.assertEqual(self.environment['id'], session['environment_id'])

    @decorators.attr(type='smoke')
    @decorators.idempotent_id('a2782f54-9f9a-443b-97be-edc17039aea5')
    def test_delete_session(self):
        session = self.application_catalog_client.\
            create_session(self.environment['id'])
        self.application_catalog_client.delete_session(self.environment['id'],
                                                       session['id'])

    @decorators.idempotent_id('0639a8ef-f527-4a5d-b34a-4e2d46f48b30')
    def test_get_session(self):
        session = self.application_catalog_client.\
            create_session(self.environment['id'])
        self.addCleanup(self.application_catalog_client.delete_session,
                        self.environment['id'], session['id'])
        session_from_resp = self.application_catalog_client.\
            get_session(self.environment['id'], session['id'])
        # Deleting dates from dictionaries to skip it in assert
        session.pop('updated', None)
        session.pop('created', None)
        session_from_resp.pop('updated', None)
        session_from_resp.pop('created', None)
        self.assertEqual(session, session_from_resp)
