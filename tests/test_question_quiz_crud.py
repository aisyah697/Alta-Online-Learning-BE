import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_mentee_user, create_token_admin_academic, create_token_admin_business, create_token_admin_council,init_database

class TestQuestionQuiz():
    def test_get_question_quis_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/questionquiz/1',
                        headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_question_quis_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/questionquiz/100',
                        headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_get_question_quis_by_id_admin_no_access(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/questionquiz/1',
                        headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_post_question_quis(self, client, init_database):
        token = create_token_admin()
        data = {
                "quiz_id" : 1,
                "question" : "Where is the most Volcano in the highest Volcano ?"
                }
        res = client.post('/questionquiz',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_post_question_quis_id_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
                "quiz_id" : 10,
                "question" : "Where is the most Volcano in the highest Volcano ?"
                }
        res = client.post('/questionquiz',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_post_question_quis_admin_no_access(self, client, init_database):
        token = create_token_admin_business()
        data = {
                "quiz_id" : 1,
                "question" : "Where is the most Volcano in the highest Volcano ?"
                }
        res = client.post('/questionquiz',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_put_question_quis(self, client, init_database):
        token = create_token_admin_business()
        data = {
                "status" : False,
                }
        res = client.put('/questionquiz/1',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_put_question_quis_data_not_found(self, client, init_database):
        token = create_token_admin_business()
        data = {
                "status" : False,
                }
        res = client.put('/questionquiz/10',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_patch_question_quis_not_found(self, client, init_database):
        token = create_token_admin()
        data = {
                "quiz_id" : 1,
                "question" : "Where?"
                }
        res = client.patch('/questionquiz/10',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_patch_question_quis_admin_no_access(self, client, init_database):
        token = create_token_admin_business()
        data = {
                "quiz_id" : 1,
                "question" : "Where?"
                }
        res = client.patch('/questionquiz/2',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_patch_question_quis(self, client, init_database):
        token = create_token_admin()
        data = {
                "quiz_id" : 1,
                "question" : "Where?"
                }
        res = client.patch('/questionquiz/1',
                        data=json.dumps(data),
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_question_quis_all(self, client, init_database):
        token = create_token_admin()
        res = client.get('/questionquiz',
                        headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_question_quis_all(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/questionquiz',
                        headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_get_question_quis_all_order_question_desc(self, client, init_database):
        token = create_token_admin()
        data = {
                "orderby": "question",
                "sort":"desc"
                }
        res = client.get('/questionquiz',
                        headers={'Authorization': 'Bearer ' + token}, 
                        query_string=data, 
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_question_quis_all_order_question_asc(self, client, init_database):
        token = create_token_admin()
        data = {
                "orderby": "question",
                "sort":"asc"
                }
        res = client.get('/questionquiz',
                        headers={'Authorization': 'Bearer ' + token}, 
                        query_string=data, 
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_question_quis_all_order_created_at_asc(self, client, init_database):
        token = create_token_admin()
        data = {
                "orderby": "created_at",
                "sort":"asc"
                }
        res = client.get('/questionquiz',
                        headers={'Authorization': 'Bearer ' + token}, 
                        query_string=data, 
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_question_quis_all_order_created_at_desc(self, client, init_database):
        token = create_token_admin()
        data = {
                "orderby": "created_at",
                "sort":"desc"
                }
        res = client.get('/questionquiz',
                        headers={'Authorization': 'Bearer ' + token}, 
                        query_string=data, 
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_question_quis_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/questionquiz/all',
                        headers={'Authorization': 'Bearer ' + token}, 
                        content_type='application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_question_quis_no_acsess(self, client, init_database):
        token = create_token_admin_business()
        res = client.delete('/questionquiz/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_delete_question_quis(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/questionquiz/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_question_quis_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.delete('/questionquiz/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    