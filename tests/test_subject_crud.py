import json 
from . import app, client, cache, create_token_admin, create_token_mentee, create_token_admin_academic, create_token_admin_business, create_token_admin_council, init_database

class TestSubjecteCrud():
    def test_get_subject_by_id(self, client, init_database):
        token = create_token_admin()
        res = client.get('/subject/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_subject_by_id_not_found(self, client, init_database):
        token = create_token_admin()
        res = client.get('/subject/9',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_get_subject_role_no_access(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/subject/1',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

# =============== post =========================================
    def test_post_subject_success(self, client, init_database):
            token = create_token_admin()
            data={
                "module_id":1,
                "name":"Algorithm 2",
                "description":"Ini pelajaran yang sangat seru loh",
                "quesioner":"Good",
                "status":True,
            }
            res = client.post('/subject',
                            data=json.dumps(data),
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            res_json = json.loads(res.data)
            assert res.status_code == 200

    def test_post_subject_module_not_found(self, client, init_database):
            token = create_token_admin()
            data={
                "module_id":5,
                "name":"Algorithm 2",
                "description":"Ini pelajaran yang sangat seru loh",
                "quesioner":"Good",
                "status":True,
            }
            res = client.post('/subject',
                            data=json.dumps(data),
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            res_json = json.loads(res.data)
            assert res.status_code == 404

    def test_post_subject_no_access_role_admin(self, client, init_database):
            token = create_token_admin_business()
            data={
                "module_id":1,
                "name":"Algorithm 3",
                "description":"Ini pelajaran yang sangat seru loh",
                "quesioner":"Good",
                "status":True,
            }
            res = client.post('/subject',
                            data=json.dumps(data),
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            res_json = json.loads(res.data)
            assert res.status_code == 404

# ================ put ==================================================
    def test_put_subject_success(self, client, init_database):
            token = create_token_admin()
            data={
                "status":False,
            }
            res = client.put('/subject/1',
                            data=json.dumps(data),
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            res_json = json.loads(res.data)
            assert res.status_code == 200
    
    def test_put_subject_id_not_found(self, client, init_database):
            token = create_token_admin()
            data={
                "status":False,
            }
            res = client.put('/subject/10',
                            data=json.dumps(data),
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            res_json = json.loads(res.data)
            assert res.status_code == 404

# ================ patch ==================================================
    def test_patch_subject_success(self, client, init_database):
            token = create_token_admin()
            data={
                "name":"CSS",
                "description":"Ini pelajaran yang sangat seru dan OK",
                "quesioner":"Very Good",
            }
            res = client.patch('/subject/1',
                            data=json.dumps(data),
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            res_json = json.loads(res.data)
            assert res.status_code == 200
    
    def test_patch_subject_id_not_found(self, client, init_database):
            token = create_token_admin()
            data={
                "name":"HTML",
            }
            res = client.patch('/subject/10',
                            data=json.dumps(data),
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            res_json = json.loads(res.data)
            assert res.status_code == 404

    def test_patch_subject_admin_no_access(self, client, init_database):
            token = create_token_admin_business()
            data={
                "name":"HTML",
            }
            res = client.patch('/subject/1',
                            data=json.dumps(data),
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            res_json = json.loads(res.data)
            assert res.status_code == 404
    
#============== subject all ===========================
    def test_get_subject_all(self, client, init_database):
        token = create_token_admin()
        res = client.get('/subject',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_subject_all_fail(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/subject',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_get_subject_all_orderby_name_desc(self, client, init_database):
        token = create_token_admin()
        res = client.get('/subject',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'name', 'sort': 'desc'},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_subject_all_orderby_name_asc(self, client, init_database):
        token = create_token_admin()
        res = client.get('/subject',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'name', 'sort': 'asc'},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_subject_all_orderby_moduleID_asc(self, client, init_database):
        token = create_token_admin()
        res = client.get('/subject',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'module_id', 'sort': 'asc'},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_subject_all_orderby_moduleID_desc(self, client, init_database):
        token = create_token_admin()
        res = client.get('/subject',
                        headers={'Authorization': 'Bearer ' + token},
                        query_string={'orderby':'module_id', 'sort': 'desc'},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

# ================ get nested by id ======================
    def test_get_subject_nested_by_id(self, client, init_database):
            token = create_token_admin()
            res = client.get('/subject/nested/1',
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'multipart/form-data')
            res_json = json.loads(res.data)
            assert res.status_code == 200
            

    def test_get_subject_nested_by_id_fail(self, client, init_database):
            token = create_token_admin_business()
            res = client.get('/subject/nested/1',
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'multipart/form-data')
            res_json = json.loads(res.data)
            assert res.status_code == 404

# ================ get nested all ===================
    def test_get_subject_all_nested(self, client, init_database):
        token = create_token_admin()
        res = client.get('/subject/nested',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_subject_all_nested_fail(self, client, init_database):
        token = create_token_admin_business()
        res = client.get('/subject/nested',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 404

# ================ get status all ===================
    def test_get_subject_all_status(self, client, init_database):
        token = create_token_admin()
        res = client.get('/subject/all',
                        headers={'Authorization': 'Bearer ' + token},
                        content_type = 'multipart/form-data')
        res_json = json.loads(res.data)
        assert res.status_code == 200

# ================ delete ==================================================
    def test_delete_subject_success(self, client, init_database):
            token = create_token_admin()
            res = client.delete('/subject/2',
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            res_json = json.loads(res.data)
            assert res.status_code == 200

    def test_delete_subject_not_found(self, client, init_database):
            token = create_token_admin()
            res = client.delete('/subject/20',
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            res_json = json.loads(res.data)
            assert res.status_code == 404

    def test_delete_subject_no_accsess(self, client, init_database):
            token = create_token_admin_business()
            res = client.delete('/subject/1',
                            headers={'Authorization': 'Bearer ' + token},
                            content_type = 'application/json')
            res_json = json.loads(res.data)
            assert res.status_code == 404