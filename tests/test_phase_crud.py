import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestPhaseCrud():
    def test_phase_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/phase/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_phase_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/phase/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_phase_get_by_id_not_admin_super_and_academic(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/phase/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_phase_post_admin_super(self, client, init_database):
        token = create_token_admin()
        data = {
            'name': 'Phase 3',
            'description': "Lorem Ipsum Dolor",
            'status': True
        }
        res = client.post('/phase', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data),content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_post_admin_not_super(self, client, init_database):
        token = create_token_admin_business()
        data = {
            'name': 'Phase 3',
            'description': "Lorem Ipsum Dolor",
            'status': True
        }
        res = client.post('/phase', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data),content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_phase_put(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/phase/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_put_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/phase/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_phase_patch(self, client, init_database):
        token = create_token_admin()
        data = {
            'description': "Lorem Ipsum Dolor 1",
        }
        res = client.patch('/phase/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_patch_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            'description': "Lorem Ipsum Dolor 1",
        }
        res = client.patch('/phase/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_phase_patch_admin_not_super(self, client, init_database):
        token = create_token_admin_business()
        data = {
            'description': "Lorem Ipsum Dolor 1",
        }
        res = client.patch('/phase/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_phase_delete(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/phase/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_delete_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/phase/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_phase_delete_admin_not_super(self, client, init_database):
        token = create_token_admin_business()
        res = client.delete('/phase/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_phase_get_all_status_true_id_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'id', 
            'sort': 'desc'
        }
        res = client.get('/phase', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_get_all_status_true_id_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'id', 
            'sort': 'asc'
        }
        res = client.get('/phase', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_get_all_status_true_createdat_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'desc'
        }
        res = client.get('/phase', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_get_all_status_true_createdat_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'asc'
        }
        res = client.get('/phase', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_get_all_status_true_admin_not_super_academic(self, client, init_database):
        token = create_token_admin_business()
        data={
            'orderby': 'created_at', 
            'sort': 'asc'
        }
        res = client.get('/phase', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_phase_get_nested_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/phase/nested/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_get_nested_by_id_admin_not_super_academic(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/phase/nested/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_phase_get_nested_id_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'id', 
            'sort': 'desc'
        }
        res = client.get('/phase/nested', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_get_nested_id_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'id', 
            'sort': 'asc'
        }
        res = client.get('/phase/nested', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_get_nested_createdat_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'desc'
        }
        res = client.get('/phase/nested', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_get_nested_createdat_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'asc'
        }
        res = client.get('/phase/nested', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_phase_get_nested_admin_not_super_academic(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/phase/nested', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_phase_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/phase/all', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200