import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestReviewModulCrud():
    def test_review_module_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/reviewmodule/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_review_module_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/reviewmodule/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_review_module_post_ever_submit(self, client, init_database):
        token = create_token_admin()
        data={
            "mentee_id": 1,
            "module_id": 1,
            "content": "Lorem Ipsum",
            "score": 4,
            "status": True
        }
        res = client.post('/reviewmodule', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_review_module_post(self, client, init_database):
        token = create_token_admin()
        data={
            "mentee_id": 2,
            "module_id": 1,
            "content": "Lorem Ipsum",
            "score": 4,
            "status": True
        }
        res = client.post('/reviewmodule', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_review_module_put(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/reviewmodule/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_review_module_put_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/reviewmodule/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_review_module_patch(self, client, init_database):
        token = create_token_admin()
        data={
            "mentee_id": 2,
            "module_id": 1,
            "content": "Lorem Ipsum",
            "score": 4,
        }
        res = client.patch('/reviewmodule/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_review_module_patch_id_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "mentee_id": 2,
            "module_id": 1,
            "content": "Lorem Ipsum",
            "score": 4,
        }
        res = client.patch('/reviewmodule/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_review_module_delete(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/reviewmodule/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_review_module_delete_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/reviewmodule/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_review_module_get_all_status_true_modulid_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'module_id', 
            'sort': 'desc'
        }
        res = client.get('/reviewmodule', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_review_module_get_all_status_true_modulid_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'module_id', 
            'sort': 'asc'
        }
        res = client.get('/reviewmodule', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200
    
    def test_review_module_get_all_status_true_score_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'score', 
            'sort': 'desc'
        }
        res = client.get('/reviewmodule', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_review_module_get_all_status_true_score_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'score', 
            'sort': 'asc'
        }
        res = client.get('/reviewmodule', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_review_module_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/reviewmodule/all', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200