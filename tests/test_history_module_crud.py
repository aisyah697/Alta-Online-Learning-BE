import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_mentee_user, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestHistoryModuleCrud():
    def test_history_module_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/historymodule/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_module_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/historymodule/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_module_post(self, client, init_database):
        token = create_token_mentee()
        data = {
            "module_id": 1,
            "mentee_id": 2
        }
        res = client.post('/historymodule', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_module_post_mentee_already_register(self, client, init_database):
        token = create_token_mentee()
        data = {
            "module_id": 1,
            "mentee_id": 1
        }
        res = client.post('/historymodule', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_module_post_mentee_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "module_id": 1,
            "mentee_id": 100
        }
        res = client.post('/historymodule', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_module_post_module_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "module_id": 100,
            "mentee_id": 1
        }
        res = client.post('/historymodule', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_module_put(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/historymodule/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_module_put_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/historymodule/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_module_patch(self, client, init_database):
        token = create_token_mentee()
        data = {
            "mentee_id": 2,
            "module_id": 1,
            "score": 80,
            "is_complete": True,
            "lock_key": True

        }
        res = client.patch('/historymodule/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_module_patch_id_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "mentee_id": 2,
            "module_id": 1,
            "score": 80,
            "is_complete": True,
            "lock_key": True

        }
        res = client.patch('/historymodule/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_module_delete(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/historymodule/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_module_delete_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/historymodule/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_module_get_all_status_true_score_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'score', 
            'sort': 'desc'
        }
        res = client.get('/historymodule', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_module_get_all_status_true_score_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'score', 
            'sort': 'asc'
        }
        res = client.get('/historymodule', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_module_get_all_status_true_created_at_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'desc'
        }
        res = client.get('/historymodule', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_module_get_all_status_true_created_at_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'asc'
        }
        res = client.get('/historymodule', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_module_get_by_token_mentee(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/historymodule/mentee', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_module_post_by_token_mentee(self, client, init_database):
        token = create_token_mentee_user()
        res = client.post('/historymodule/mentee', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_module_post_by_token_mentee_already_register(self, client, init_database):
        token = create_token_mentee()
        res = client.post('/historymodule/mentee', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_module_post_by_token_mentee_by_id_phase(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/historymodule/subject/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_module_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/historymodule/all', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200