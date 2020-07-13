import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestExamCrud():
    def test_exam_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/exam/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_exam_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/exam/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_exam_get_by_id_not_super_academic(self, client, init_database):
        token = create_token_admin_council()
        res = client.get('/exam/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_exam_post(self, client, init_database):
        token = create_token_admin()
        data={
            "subject_id": 4,
            "type_exam": "quiz",
            "status": True
        }
        res = client.post('/exam', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_exam_post_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data={
            "subject_id": 1,
            "type_exam": "quiz",
            "status": True
        }
        res = client.post('/exam', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_exam_post_subject_id_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "subject_id": 100,
            "type_exam": "quiz",
            "status": True
        }
        res = client.post('/exam', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_exam_post_subject_id_have_another_exam(self, client, init_database):
        token = create_token_admin()
        data={
            "subject_id": 1,
            "type_exam": "quiz",
            "status": True
        }
        res = client.post('/exam', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_exam_put(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/exam/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_exam_put_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/exam/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_exam_patch(self, client, init_database):
        token = create_token_admin()
        data = {
            "subject_id": 1,
            "type_exam": "livecode",
        }
        res = client.patch('/exam/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_exam_patch_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "subject_id": 1,
            "type_exam": "livecode",
        }
        res = client.patch('/exam/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_exam_patch_id_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data = {
            "subject_id": 1,
            "type_exam": "livecode",
        }
        res = client.patch('/exam/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_exam_delete(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/exam/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_exam_delete_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/exam/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_exam_delete_id_admin_business(self, client, init_database):
        token = create_token_admin_business()
        res = client.delete('/exam/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_exam_get_all_status_true_subjectid_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'subject_id', 
            'sort': 'desc'
        }
        res = client.get('/exam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_exam_get_all_status_true_subjectid_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'subject_id', 
            'sort': 'asc'
        }
        res = client.get('/exam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_exam_get_all_status_true_typeexam_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'type_exam', 
            'sort': 'desc'
        }
        res = client.get('/exam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_exam_get_all_status_true_typeexam_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'type_exam', 
            'sort': 'asc'
        }
        res = client.get('/exam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_exam_get_all_status_true_admin_not_super_academic(self, client, init_database):
        token = create_token_admin_business()
        data={
            'orderby': 'type_exam', 
            'sort': 'asc'
        }
        res = client.get('/exam', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_exam_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/exam/all', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200