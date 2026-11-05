import os, tempfile, unittest
import app as module

class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False); self.tmp.close()
        self.old_db = module.DB; module.DB = self.tmp.name
        module.init_db(); module.app.config.update(TESTING=True, SECRET_KEY='test-secret')
        self.client = module.app.test_client()
    def tearDown(self):
        module.DB = self.old_db; os.unlink(self.tmp.name)
    def token(self):
        with self.client.session_transaction() as s: return s['csrf']
    def test_dashboard_requires_login(self): self.assertEqual(self.client.get('/dashboard').status_code, 302)
    def test_post_requires_csrf(self): self.assertEqual(self.client.post('/login', data={'username':'x'}).status_code, 400)
    def test_register_login_dashboard(self):
        r=self.client.post('/register',data={'csrf':self.token(),'username':'demo_user','password':'StrongPass123!'},follow_redirects=True)
        self.assertEqual(r.status_code,200)
        r=self.client.post('/login',data={'csrf':self.token(),'username':'demo_user','password':'StrongPass123!'},follow_redirects=True)
        self.assertIn(b'Session active',r.data)
if __name__=='__main__': unittest.main()
