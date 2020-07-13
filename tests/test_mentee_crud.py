import json 
from . import app, client, cache, create_token_admin, create_token_mentee, init_database

class TestMenteeCrud():
    def test_mentee_get_by_id(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/mentee/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_mentee_get_by_id_not_found(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/mentee/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_mentee_post(self, client, init_database):
        token = create_token_mentee()
        data = {
            "username": "aisyah697",
            "password": "password",
            "full_name": "Aisyah PU",
            "email": "aisyah@gmail.com",
            "address": "Depok",
            "phone": "0815568529",
            "place_birth": "Jakarta",
            "date_birth": "28 Juni 1994",
            "avatar": "hsjkkd.jpg",
            "background_education": "geoscience",
            "github": "www.github/aisyah697",
            "description": "lorem ipsum",
            "salt": "suhdushdushdus78378y",
            "status": True
        }
        res = client.post('/mentee', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_post_username_exist(self, client, init_database):
        token = create_token_mentee()
        data = {
            "username": "rosliani12",
            "password": "password"
        }
        res = client.post('/mentee', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_post_username_less_6_char(self, client, init_database):
        token = create_token_mentee()
        data = {
            "username": "rosli",
            "password": "password"
        }
        res = client.post('/mentee', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_post_password_less_6_char(self, client, init_database):
        token = create_token_mentee()
        data = {
            "username": "aisyah",
            "password": "pass"
        }
        res = client.post('/mentee', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_post_telephon_not_allow(self, client, init_database):
        token = create_token_mentee()
        data = {
            "username": "aisyah",
            "password": "password",
            "phone": "0815"
        }
        res = client.post('/mentee', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_post_email_not_allow(self, client, init_database):
        token = create_token_mentee()
        data = {
            "username": "aisyah",
            "password": "password",
            "email": "ajiohohjjuh"
        }
        res = client.post('/mentee', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_post_status_false(self, client, init_database):
        token = create_token_mentee()
        data = {
            "username": "aisyah",
            "password": "password",
            "full_name": "aisyah pu",
            "email": "aisyah@gmail.com",
            "address": "Depok",
            "phone": "0815568529",
            "place_birth": "Jakarta",
            "date_birth": "28 Juni 1994",
            "avatar": "hsjkkd.jpg",
            "background_education": "geoscience",
            "github": "www.github/aisyah697",
            "description": "lorem ipsum",
            "salt": "suhdushdushdus78378y",
            "status": False
        }
        res = client.post('/mentee', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_put_false(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": False
        }
        res = client.put('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_put_true(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_put_id_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
            "status": True
        }
        res = client.put('/mentee/100', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_put_id_not_fill(self, client, init_database):
        token = create_token_mentee()
        data = {
        }
        res = client.put('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_patch(self, client, init_database):
        token = create_token_mentee()
        data = {
            "full_name": "aisyah pu",
            "address": "Depok",
            "place_birth": "Jakarta",
            "date_birth": "28 Juni 1994",
            "background_education": "geoscience",
            "github": "www.github/aisyah697",
            "description": "lorem ipsum"
        }
        res = client.patch('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_patch_id_not_found(self, client, init_database):
        token = create_token_mentee()
        data = {
        }
        res = client.patch('/mentee/100', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_patch_username(self, client, init_database):
        token = create_token_mentee()
        data = {
            "username": "aisyah"
        }
        res = client.patch('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_patch_username_less_6_char(self, client, init_database):
        token = create_token_mentee()
        data = {
            "username": "aisy"
        }
        res = client.patch('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_patch_password(self, client, init_database):
        token = create_token_mentee()
        data = {
            "password": "lolipop"
        }
        res = client.patch('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_patch_password_less_6_char(self, client, init_database):
        token = create_token_mentee()
        data = {
            "password": "loli"
        }
        res = client.patch('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_patch_email(self, client, init_database):
        token = create_token_mentee()
        data = {
            "email": "pangestu@alterra.id"
        }
        res = client.patch('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_patch_email_not_allowed(self, client, init_database):
        token = create_token_mentee()
        data = {
            "email": "uhduhdud"
        }
        res = client.patch('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_patch_phone(self, client, init_database):
        token = create_token_mentee()
        data = {
            "phone": "08155685291"
        }
        res = client.patch('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_patch_phone_not_allowed(self, client, init_database):
        token = create_token_mentee()
        data = {
            "phone": "98718768632432342343286"
        }
        res = client.patch('/mentee/1', headers={'Authorization': 'Bearer ' + token}, data=data, content_type='multipart/form-data')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_get_history_score_mentee(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/mentee/score/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_get_history_score_mentee_not_found(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/mentee/score/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==404

    def test_mentee_get_all_status_true_username_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'username', 
            'sort': 'desc'
        }
        res = client.get('/mentee', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_get_all_status_true_username_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'username', 
            'sort': 'asc'
        }
        res = client.get('/mentee', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_get_all_status_true_fullname_desc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'full_name', 
            'sort': 'desc'
        }
        res = client.get('/mentee', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_get_all_status_true_fullname_asc(self, client, init_database):
        token = create_token_admin()
        data={
            'orderby': 'full_name', 
            'sort': 'asc'
        }
        res = client.get('/mentee', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_get_all_status_true_search(self, client, init_database):
        token = create_token_admin()
        data={
            'search': 'rosli'
        }
        res = client.get('/mentee', headers={'Authorization': 'Bearer ' + token}, query_string=data, content_type='application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_mentee_get_all_status(self, client, init_database):
        token = create_token_mentee()
        res = client.get('/mentee/all', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
        res_json=json.loads(res.data)
        assert res.status_code==200


#     # def test_mentee_delete_by_id(self, client, init_database):
#     #     token = create_token_mentee()
#     #     res = client.delete('/mentee/1', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
#     #     res_json = json.loads(res.data)
#     #     assert res.status_code == 200

#     # def test_mentee_delete_by_id_not_found(self, client, init_database):
#     #     token = create_token_mentee()
#     #     res = client.delete('/mentee/100', headers={'Authorization': 'Bearer ' + token}, content_type = 'application/json')
#     #     res_json=json.loads(res.data)
#     #     assert res.status_code==404