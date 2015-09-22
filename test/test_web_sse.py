# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2015 SciFabric LTD.
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.
from helper import web
from default import with_context
from factories import ProjectFactory, UserFactory
from pybossa.core import user_repo

class TestWebSse(web.Helper):


    @with_context
    def test_stream_uri_private_anon(self):
        """Test stream URI private anon works."""
        project = ProjectFactory.create()
        private_uri = '/project/%s/privatestream' % project.short_name
        res = self.app.get(private_uri, follow_redirects=True)
        assert res.status_code == 200, res.status_code
        assert 'Please sign in to access this page' in res.data, res.data

    @with_context
    def test_stream_uri_private_auth(self):
        """Test stream URI private auth but not owner works."""
        self.register()
        user = user_repo.get(1)
        project = ProjectFactory.create(owner=user)
        self.signout()
        self.register(fullname='Juan', name='juan', password='juana')
        private_uri = '/project/%s/privatestream' % project.short_name
        res = self.app.get(private_uri, follow_redirects=True)
        assert res.status_code == 403, res.data
