import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council, create_token_mentee_user, init_database

class TestCorrectionAltatestCrud():
    def test_correction_altatest_get(self, client, init_database):
        token = create_token_mentee()
        data = {
            "question_altatest_id": 1
        }
        res = client.get('/correctionaltatest', headers={'Authorization': 'Bearer ' + token}, data=json.dumps(data), content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_correction_altatest_delete_by_id(self, client, init_database):
        token = create_token_mentee()
        res = client.delete('/correctionaltatest/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_correction_altatest_delete_by_id_not_found(self, client, init_database):
        token = create_token_mentee()
        res = client.delete('/correctionaltatest/111', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404