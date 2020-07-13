import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestQuestionAltatestCrud():
    def test_question_altatest_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/questionaltatest/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_question_altatest_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/questionaltatest/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_question_altatest_post(self, client, init_database):
        token = create_token_admin()
        data={
            "admin_id": 1,
            "question": "What is Python ?",
            "status": True
        }
        res = client.post('/questionaltatest', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_question_altatest_post_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data={
            "admin_id": 1,
            "question": "What is Python ?",
            "status": True
        }
        res = client.post('/questionaltatest', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_question_altatest_put(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/questionaltatest/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_question_altatest_put_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/questionaltatest/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_question_altatest_patch(self, client, init_database):
        token = create_token_admin()
        data = {
            "question": "What is Flask ?"
        }
        res = client.patch('/questionaltatest/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_question_altatest_patch_admin_business(self, client, init_database):
        token = create_token_admin_business()
        data = {
            "question": "What is Flask ?"
        }
        res = client.patch('/questionaltatest/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_question_altatest_patch_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "question": "What is Flask ?"
        }
        res = client.patch('/questionaltatest/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_question_altatest_delete(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/questionaltatest/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_question_altatest_delete_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/questionaltatest/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_question_altatest_delete_admin_business(self, client, init_database):
        token = create_token_admin_business()
        res = client.delete('/questionaltatest/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_question_altatest_get_all_status_true_question_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'question', 
            'sort': 'desc'
        }
        res = client.get('/questionaltatest', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_question_altatest_get_all_status_true_question_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'question', 
            'sort': 'asc'
        }
        res = client.get('/questionaltatest', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_question_altatest_get_all_status_true_createdat_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'desc'
        }
        res = client.get('/questionaltatest', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_question_altatest_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/questionaltatest/all', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200
