import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestFileSubjectCrud():
    def test_file_subject_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/filesubject/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_file_subject_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/filesubject/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_file_subject_get_by_id_admin_business(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/filesubject/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    # def test_file_subject_post(self, client, init_database):
    #     token = create_token_admin()
    #     data={
    #         "subject_id": 1,
    #         "name": "Debugging 1",
    #         "content_file": "/home/alta3/Pictures/index.jpeg",
    #         "category_file": "video"
    #     }
    #     res = client.post('/filesubject', headers={'Authorization': 'Bearer ' + token}, data=data,content_type = 'multipart/form-data')
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    def test_file_subject_put_true(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/filesubject/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type = 'multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_file_subject_put_false(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": False
        }
        res = client.put('/filesubject/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type = 'multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_file_subject_put_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/filesubject/100', headers={'Authorization': 'Bearer ' + token}, data=data, content_type = 'multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_file_subject_patch(self, client, init_database):
        token = create_token_admin()
        data={
            "subject_id": 1,
            "name": "Debugging 1",
            "content_file": "/home/alta3/Pictures/index.jpeg",
            "category_file": "video"
        }
        res = client.patch('/filesubject/1', headers={'Authorization': 'Bearer ' + token}, data=data,content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_file_subject_patch_id_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "subject_id": 1,
            "name": "Debugging 1",
            "content_file": "/home/alta3/Pictures/index.jpeg",
            "category_file": "video"
        }
        res = client.patch('/filesubject/100', headers={'Authorization': 'Bearer ' + token}, data=data,content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_file_subject_patch_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data={
            "subject_id": 1,
            "name": "Debugging 1",
            "content_file": "/home/alta3/Pictures/index.jpeg",
            "category_file": "video"
        }
        res = client.patch('/filesubject/1', headers={'Authorization': 'Bearer ' + token}, data=data,content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_file_subject_get_all_status_true_subject_id_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'subject_id', 
            'sort': 'desc'
        }
        res = client.get('/filesubject', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_file_subject_get_all_status_true_subject_id_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'subject_id', 
            'sort': 'asc'
        }
        res = client.get('/filesubject', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_file_subject_get_all_status_true_category_file_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'category_file', 
            'sort': 'desc'
        }
        res = client.get('/filesubject', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_file_subject_get_all_status_true_category_file_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'category_file', 
            'sort': 'asc'
        }
        res = client.get('/filesubject', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_file_subject_get_all_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data={
            'orderby': 'subject_id', 
            'sort': 'asc'
        }
        res = client.get('/filesubject', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_file_subject_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/filesubject/all', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200