import json 
from . import app, client, cache, create_token_admin, create_token_mentee, init_database

class TestAdminCrud():
    def test_admin_get_by_Id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200