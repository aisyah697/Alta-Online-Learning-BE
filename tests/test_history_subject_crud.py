import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_mentee_user, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestHistorySubjectCrud():
    def test_history_subject_get_by_id(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/historysubject/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_subject_id_mentee_not_match(self, client, init_database):
        token = create_token_mentee_user()
        res = client.get('/historysubject/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_subject_get_by_id_not_found(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/historysubject/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_subject_post(self, client, init_database):
        token = create_token_mentee()
        data = {
            "subject_id": 1,
            "mentee_id": 2,
            "score": 80
        }
        res = client.post('/historysubject', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_subject_post_score_not_pass(self, client, init_database):
        token = create_token_mentee()
        data = {
            "subject_id": 1,
            "mentee_id": 2,
            "score": 8
        }
        res = client.post('/historysubject', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_subject_post_mentee_already_register(self, client, init_database):
        token = create_token_mentee()
        data = {
            "subject_id": 1,
            "mentee_id": 1
        }
        res = client.post('/historysubject', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_subject_post_mentee_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "subject_id": 1,
            "mentee_id": 100
        }
        res = client.post('/historysubject', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_subject_post_subject_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "subject_id": 100,
            "mentee_id": 1
        }
        res = client.post('/historysubject', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_subject_put(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/historysubject/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_subject_put_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/historysubject/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_subject_patch(self, client, init_database):
        token = create_token_mentee()
        data = {
            "subject_id": 1,
            "mentee_id": 2,
            "score": 85,
            "time_of_exam": 1
        }
        res = client.patch('/historysubject/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_subject_patch_score_not_pass(self, client, init_database):
        token = create_token_mentee()
        data = {
            "subject_id": 1,
            "mentee_id": 2,
            "score": 78,
            "time_of_exam": 1
        }
        res = client.patch('/historysubject/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_subject_patch_id_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "subject_id": 1,
            "mentee_id": 2,
            "score": 85,
        }
        res = client.patch('/historysubject/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_subject_delete(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/historysubject/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_subject_delete_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/historysubject/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_subject_get_all_status_true_score_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'score', 
            'sort': 'desc'
        }
        res = client.get('/historysubject', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_subject_get_all_status_true_score_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'score', 
            'sort': 'asc'
        }
        res = client.get('/historysubject', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_subject_get_all_status_true_created_at_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'desc'
        }
        res = client.get('/historysubject', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_subject_get_all_status_true_created_at_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'asc'
        }
        res = client.get('/historysubject', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_subject_get_by_token_mentee(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/historysubject/mentee', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_subject_post_by_token_mentee(self, client, init_database):
        token = create_token_mentee_user()
        res = client.post('/historysubject/mentee', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_subject_post_by_token_mentee_already_take_course(self, client, init_database):
        token = create_token_mentee()
        res = client.post('/historysubject/mentee', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_history_subject_post_by_token_mentee_by_id_module(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/historysubject/subject/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_subject_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/historysubject/all', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200