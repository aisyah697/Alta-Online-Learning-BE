import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestRequirementModulCrud():
    def test_requirement_module_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/requirementmodule/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_requirement_module_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/requirementmodule/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_review_module_post(self, client, init_database):
        token = create_token_admin()
        data={
            "module_id": 1,
            "description": "Lorem Ipsum",
            "status": True
        }
        res = client.post('/requirementmodule', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_requirement_module_put(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/requirementmodule/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_requirement_module_put_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/requirementmodule/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_requirement_module_patch(self, client, init_database):
        token = create_token_admin()
        data={
            "description": "Lorem Ipsum",
        }
        res = client.patch('/requirementmodule/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_review_module_patch_id_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "description": "Lorem Ipsum",
        }
        res = client.patch('/requirementmodule/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_requirement_module_delete(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/requirementmodule/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_requirement_module_delete_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/requirementmodule/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_requirement_module_get_all_status_true_module_id_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'module_id', 
            'sort': 'desc'
        }
        res = client.get('/requirementmodule', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_requirement_module_get_all_status_true_module_id_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'module_id', 
            'sort': 'asc'
        }
        res = client.get('/requirementmodule', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200
    
    def test_review_module_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/requirementmodule/all', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200