import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council, init_database

class TestAdminCrud():
    def test_admin_get_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_admin_get_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin/100',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_post_admin_username_already_exist(self, client, init_database):
        token = create_token_admin()
        data={
            "username": "umam12",
            "password": "yopiragil",
            "full_name": "Yopi Ragil P",
            "role": "super",
            "email": "yopi@gmail.com",
            "address": "Jombang",
            "phone": "08262534535266",
            "place_birth": "Jombang",
            "date_birth": "10 November 19994",
            "github": "www.github.com/yopiragil",
            "description": "saya suka koding",
            "status": True,
            }
        res = client.post('/admin',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_post_admin_username_less_than_6character(self, client, init_database):
        token = create_token_admin()
        data={
            "username": "yopi",
            "password": "yopiragil",
            "full_name": "Yopi Ragil P",
            "role": "super",
            "email": "yopi@gmail.com",
            "address": "Jombang",
            "phone": "08262534535266",
            "place_birth": "Jombang",
            "date_birth": "10 November 19994",
            "github": "www.github.com/yopiragil",
            "description": "saya suka koding",
            "status": True,
            }
        res = client.post('/admin',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_post_admin_phone_wrong(self, client, init_database):
        token = create_token_admin()
        data={
            "username": "yopiragil",
            "password": "yopiragil",
            "full_name": "Yopi Ragil P",
            "role": "super",
            "email": "yopi@gmail.com",
            "address": "Jombang",
            "phone": "08266",
            "place_birth": "Jombang",
            "date_birth": "10 November 19994",
            "github": "www.github.com/yopiragil",
            "description": "saya suka koding",
            "status": True,
            }
        res = client.post('/admin',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_post_admin_password_less_than_6char(self, client, init_database):
        token = create_token_admin()
        data={
            "username": "yopiragil",
            "password": "yo",
            "full_name": "Yopi Ragil P",
            "role": "super",
            "email": "yopi@gmail.com",
            "address": "Jombang",
            "phone": "0123456789",
            "place_birth": "Jombang",
            "date_birth": "10 November 19994",
            "github": "www.github.com/yopiragil",
            "description": "saya suka koding",
            "status": True,
            }
        res = client.post('/admin',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_post_admin_email_wrong(self, client, init_database):
        token = create_token_admin()
        data={
            "username": "yopiragil",
            "password": "yopiragil",
            "full_name": "Yopi Ragil P",
            "role": "super",
            "email": "yopigmail.com",
            "address": "Jombang",
            "phone": "01234567890",
            "place_birth": "Jombang",
            "date_birth": "10 November 19994",
            "github": "www.github.com/yopiragil",
            "description": "saya suka koding",
            "status": True,
            }
        res = client.post('/admin',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_post_admin_status_true(self, client, init_database):
        token = create_token_admin()
        data={
            "username": "yopiragil",
            "password": "yopiragil",
            "full_name": "Yopi Ragil P",
            "role": "super",
            "email": "yopi@gmail.com",
            "address": "Jombang",
            "phone": "01234567890",
            "place_birth": "Jombang",
            "date_birth": "10 November 19994",
            "github": "www.github.com/yopiragil",
            "description": "saya suka koding",
            "status": True,
            }
        res = client.post('/admin',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_post_admin_status_false(self, client, init_database):
        token = create_token_admin()
        data={
            "username": "yopiragil",
            "password": "yopiragil",
            "full_name": "Yopi Ragil P",
            "role": "super",
            "email": "yopi@gmail.com",
            "address": "Jombang",
            "phone": "01234567890",
            "place_birth": "Jombang",
            "date_birth": "10 November 19994",
            "github": "www.github.com/yopiragil",
            "description": "saya suka koding",
            "status": False,
            }
        res = client.post('/admin',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_post_admin_success(self, client, init_database):
        token = create_token_admin()
        data={
            "username": "yopiragil",
            "password": "yopiragil",
            "full_name": "Yopi Ragil P",
            "role": "super",
            "email": "yopi@gmail.com",
            "address": "Jombang",
            "phone": "01234567890",
            "place_birth": "Jombang",
            "date_birth": "10 November 19994",
            "github": "www.github.com/yopiragil",
            "description": "saya suka koding",
            "status": "True",
            }
        res = client.post('/admin',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_post_admin_no_access(self, client, init_database):
        token = create_token_admin_academic()
        data={
            "username": "yopiragil",
            "password": "yopiragil",
            "full_name": "Yopi Ragil P",
            "role": "super",
            "email": "yopi@gmail.com",
            "address": "Jombang",
            "phone": "01234567890",
            "place_birth": "Jombang",
            "date_birth": "10 November 19994",
            "github": "www.github.com/yopiragil",
            "description": "saya suka koding",
            "status": "True",
            }
        res = client.post('/admin',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404


# ======================== patch=================================================


    def test_patch_admin_success(self, client, init_database):
        token = create_token_admin()
        data={
            "username": "yopi12",
            "password": "yopiragil",
            "full_name": "Yopi Ragil P",
            "role": "super",
            "email": "yopi@gmail.com",
            "address": "Jombang",
            "phone": "08262534535266",
            "place_birth": "Jombang",
            "date_birth": "10 November 19994",
            "github": "www.github.com/yopiragil",
            "description": "saya suka koding",
            "status": True,
            }
        res = client.patch('/admin/2',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_patch_admin_id_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "full_name": "Agus D S",
            }
        res = client.patch('/admin/9',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_patch_admin_password_lessthan_6char(self, client, init_database):
        token = create_token_admin()
        data={
            "password": "www",
            }
        res = client.patch('/admin/2',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_patch_admin_email_wrong(self, client, init_database):
        token = create_token_admin()
        data={
            "email": "yopigmail.com",
            }
        res = client.patch('/admin/2',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_patch_admin_phone_wrong(self, client, init_database):
        token = create_token_admin()
        data={
            "phone": "0120",
            }
        res = client.patch('/admin/2',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_patch_admin_username_less_than_6char(self, client, init_database):
        token = create_token_admin()
        data={
            "username": "yo",
            }
        res = client.patch('/admin/2',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

# ======================== put=================================================

    def test_put_admin_id_not_found(self, client, init_database):
        token = create_token_admin()
        data={
            "status": "False",
            }
        res = client.put('/admin/5',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_put_admin_status_false_success(self, client, init_database):
        token = create_token_admin()
        data={
            "status": "False",
            }
        res = client.put('/admin/2',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_put_admin_status_true_success(self, client, init_database):
        token = create_token_admin()
        data={
            "status": "true",
            }
        res = client.put('/admin/2',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_put_admin_status_no_filled(self, client, init_database):
        token = create_token_admin()
        data={}
        res = client.put('/admin/2',
                        data=data,
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
# ================ get admin all status true =============
    def test_get_admin_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin/all',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_admin_all_status_true(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_admin_no_access(self, client, init_database):
        token = create_token_admin_academic()
        res = client.get('/admin',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_get_admin_orderby_role(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'role', 'sort': 'desc'},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_admin_orderby_role_asc(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'role', 'sort': 'asc'},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_admin_orderby_username(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'username', 'sort': 'desc'},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_admin_orderby_username_asc(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'username', 'sort': 'asc'},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_admin_orderby_full_name(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'full_name', 'sort': 'desc'},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_admin_orderby_full_name_asc(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'full_name', 'sort': 'asc'},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_admin_orderby_search(self, client, init_database):
        token = create_token_admin()
        res = client.get('/admin',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'search':'kob'},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200