import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council, create_token_mentee_user, init_database

class TestHistoriyAltatestCrud():
    def test_history_altatest_get_by_id(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/historyaltatest/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_history_altatest_post_history_mentee_exist(self, client, init_database):
        token = create_token_mentee()
        data = {
            "question_sum": 1,
            "status": True
        }
        res = client.post('/historyaltatest', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 403

    def test_history_altatest_put(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/historyaltatest/1', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_altatest_put_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
            "status": True
        }
        res = client.put('/historyaltatest/100', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_altatest_patch_id_start(self, client, init_database):
        token = create_token_mentee()
        data = {
            "is_complete": "start"
        }
        res = client.patch('/historyaltatest', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_altatest_patch_id_end(self, client, init_database):
        token = create_token_mentee()
        data = {
            "is_complete": "end"
        }
        res = client.patch('/historyaltatest', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_altatest_patch_id_null(self, client, init_database):
        token = create_token_mentee()
        data = {
            "is_complete": "null"
        }
        res = client.patch('/historyaltatest', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_altatest_patch_not_register(self, client, init_database):
        token = create_token_mentee_user()
        data = {
            "is_complete": "null"
        }
        res = client.patch('/historyaltatest', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_altatest_delete(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/historyaltatest/1', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_altatest_delete_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/historyaltatest/100', headers={'Authorization': 'Bearer ' + token}, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_history_altatest_get_all_status_true_score_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'score', 
            'sort': 'desc'
        }
        res = client.get('/historyaltatest/mentee', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_altatest_get_all_status_true_score_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'score', 
            'sort': 'asc'
        }
        res = client.get('/historyaltatest/mentee', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_altatest_get_all_status_true_createdat_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'desc'
        }
        res = client.get('/historyaltatest/mentee', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_altatest_get_all_status_true_question_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'created_at', 
            'sort': 'asc'
        }
        res = client.get('/historyaltatest/mentee', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_altatest_correction(self, client, init_database):
        token = create_token_mentee()
        data = {
            "history_altatest_id": 1,
            "question_altatest_id": 1,
            "answer_id": 1
        }
        res = client.post('/historyaltatest/question', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_history_altatest_correction_not_in_database(self, client, init_database):
        token = create_token_mentee()
        data = {
            "history_altatest_id": 2,
            "question_altatest_id": 1,
            "answer_id": 1
        }
        res = client.post('/historyaltatest/question', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==403

    def test_history_altatest_correction_not_match_mentee_and_history(self, client, init_database):
        token = create_token_mentee_user()
        data = {
            "history_altatest_id": 1,
            "question_altatest_id": 1,
            "answer_id": 1
        }
        res = client.post('/historyaltatest/question', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==403

    def test_history_altatest_correction_question_not_in_database(self, client, init_database):
        token = create_token_mentee()
        data = {
            "history_altatest_id": 1,
            "question_altatest_id": 2,
            "answer_id": 1
        }
        res = client.post('/historyaltatest/question', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==403

    def test_history_altatest_correction_answer_not_in_database(self, client, init_database):
        token = create_token_mentee()
        data = {
            "history_altatest_id": 1,
            "question_altatest_id": 1,
            "answer_id": 2
        }
        res = client.post('/historyaltatest/question', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==403

    def test_history_altatest_get_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/historyaltatest/all', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200