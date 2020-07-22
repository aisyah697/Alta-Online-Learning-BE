import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestModuleCrud():
    def test_module_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/module/1', headers={'Authorization': 'Bearer ' + token},content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_module_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/module/100', headers={'Authorization': 'Bearer ' + token},content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_module_get_by_id_admin_not_super(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/module/1', headers={'Authorization': 'Bearer ' + token},content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_module_post(self, client, init_database):
        token = create_token_admin()
        data={
            "admin_id": 1,
            "phase_id": 1,
            "name": "Python X",
            "description": "Lorem Ipsum dolor dolor",
            "image": "wwww.djidjsidj.pdf",
            "status": True
        }
        res = client.post('/module', headers={'Authorization': 'Bearer ' + token}, data=data,content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_module_post_phase_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "admin_id": 1,
            "phase_id": 100,
            "name": "Python X",
            "description": "Lorem Ipsum dolor dolor",
            "image": "wwww.djidjsidj.pdf",
            "status": True
        }
        res = client.post('/module', headers={'Authorization': 'Bearer ' + token}, data=data,content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_module_post_admin_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "admin_id": 222,
            "phase_id": 1,
            "name": "Python X",
            "description": "Lorem Ipsum dolor dolor",
            "image": "wwww.djidjsidj.pdf",
            "status": True
        }
        res = client.post('/module', headers={'Authorization': 'Bearer ' + token}, data=data,content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_module_post_status_False(self, client, init_database):
        token = create_token_admin()
        data={
            "admin_id": 1,
            "phase_id": 1,
            "name": "Python X",
            "description": "Lorem Ipsum dolor dolor",
            "image": "wwww.djidjsidj.pdf",
            "status": False
        }
        res = client.post('/module', headers={'Authorization': 'Bearer ' + token}, data=data,content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_module_post_admin_not_super(self, client, init_database):
        token = create_token_admin_business()
        data={
            "admin_id": 1,
            "phase_id": 1,
            "name": "Python X",
            "description": "Lorem Ipsum dolor dolor",
            "image": "wwww.djidjsidj.pdf",
            "status": False
        }
        res = client.post('/module', headers={'Authorization': 'Bearer ' + token}, data=data, content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404


    def test_module_put_true(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/module/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type = 'multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_put_false(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": False
        }
        res = client.put('/module/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type = 'multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_put_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/module/100', headers={'Authorization': 'Bearer ' + token}, data=data, content_type = 'multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_module_patch(self, client, init_database):
        token = create_token_admin()
        data={
            "admin_id": 1,
            "phase_id": 1,
            "name": "Python X",
            "description": "Lorem Ipsum dolor dolor",
            "image": "wwww.djidjsidj.pdf"
        }
        res = client.patch('/module/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_module_patch_module_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "admin_id": 1,
            "phase_id": 1,
            "name": "Python X",
            "description": "Lorem Ipsum dolor dolor",
            "image": "wwww.djidjsidj.pdf"
        }
        res = client.patch('/module/100', headers={'Authorization': 'Bearer ' + token}, data=data, content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_module_patch_module_admin_not_super(self, client, init_database):
        token = create_token_admin_business()
        data={
            "admin_id": 1,
            "phase_id": 1,
            "name": "Python X",
            "description": "Lorem Ipsum dolor dolor",
            "image": "wwww.djidjsidj.pdf"
        }
        res = client.patch('/module/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    # def test_module_delete(self, client, init_database):
    #     token = create_token_admin()
    #     res = client.delete('/module/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
    #     res_json=json.loads(res.data)
    #     assert res.status_code==200

    # def test_module_delete_admin_not_super(self, client, init_database):
    #     token = create_token_admin_business()
    #     res = client.delete('/module/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
    #     res_json=json.loads(res.data)
    #     assert res.status_code==404

    def test_module_get_all_status_true_adminid_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'admin_id', 
            'sort': 'desc'
        }
        res = client.get('/module', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_all_status_true_adminid_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'admin_id', 
            'sort': 'asc'
        }
        res = client.get('/module', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_all_status_true_phaseid_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'phase_id', 
            'sort': 'desc'
        }
        res = client.get('/module', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_all_status_true_phaseid_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'phase_id', 
            'sort': 'asc'
        }
        res = client.get('/module', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_all_status_true_name_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'name', 
            'sort': 'desc'
        }
        res = client.get('/module', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_all_status_true_name_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'name', 
            'sort': 'asc'
        }
        res = client.get('/module', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_all_status_true_admin_not_super_academic(self, client, init_database):
        token = create_token_admin_business()
        data={
            'orderby': 'name', 
            'sort': 'asc'
        }
        res = client.get('/module', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_module_get_nested_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/module/nested/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_nested_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/module/nested/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_module_get_nested_by_id_admin_not_super_academic(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/module/nested/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_module_get_nested_adminid_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'admin_id', 
            'sort': 'desc'
        }
        res = client.get('/module/nested', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_nested_adminid_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'admin_id', 
            'sort': 'asc'
        }
        res = client.get('/module/nested', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_nested_phaseid_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'phase_id', 
            'sort': 'desc'
        }
        res = client.get('/module/nested', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_nested_phaseid_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'phase_id', 
            'sort': 'asc'
        }
        res = client.get('/module/nested', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_nested_name_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'name', 
            'sort': 'desc'
        }
        res = client.get('/module/nested', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_nested_name_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'name', 
            'sort': 'asc'
        }
        res = client.get('/module/nested', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_module_get_nested_admin_not_super_academic(self, client, init_database):
        token = create_token_admin_business()
        data={
            'orderby': 'name', 
            'sort': 'asc'
        }
        res = client.get('/module/nested', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_module_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/module/all', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200