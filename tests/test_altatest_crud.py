import json 
from . import app, client, cache, create_token_admin, create_token_mentee, init_database

class TestAltatestCrud():
    def test_altatest_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/altatest/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_altatest_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/altatest/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_altatest_post(self, client, init_database):
        token = create_token_mentee()
        data={
            "question_sum": 1,
            "status": True
        }
        res = client.post('/altatest', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_altatest_put(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/altatest/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_altatest_put_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/altatest/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_altatest_delete(self, client, init_database):
        token = create_token_mentee()
        res = client.delete('/altatest/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_altatest_delete_id_not_found(self, client, init_database):
        token = create_token_mentee()
        res = client.delete('/altatest/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_altatest_get_all_status_true_questionsum_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'question_sum', 
            'sort': 'desc'
        }
        res = client.get('/altatest', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_altatest_get_all_status_true_questionsum_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'question_sum', 
            'sort': 'asc'
        }
        res = client.get('/altatest', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_altatest_get_all_status_true_createdat_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'desc'
        }
        res = client.get('/altatest', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_altatest_get_all_status_true_createdat_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'asc'
        }
        res = client.get('/altatest', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_altatest_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/altatest/all', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200