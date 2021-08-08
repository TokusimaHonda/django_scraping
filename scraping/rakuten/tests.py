from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import resolve

from rakuten.models import Rakuten
from rakuten.views import top
UserModel = get_user_model()

class TopPageRenderRakutenTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="top_secret_pass0001",
        )
        self.rakuten = Rakuten.objects.create(
            title="title1",
            code="print('hello')",
            description="description1",
            created_by=self.user,
        )

    def test_should_return_rakuten_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.rakuten.title)

    def test_should_return_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)

class RakutenDetailTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="secret",
        )
        self.rakuten = Rakuten.objects.create(
            title="タイトル",
            code="コード",
            description="解説",
            created_by=self.user,
        )

    def test_should_use_expected_template(self):
        response = self.client.get("/rakuten/%s/" % self.rakuten.id)
        self.assertTemplateUsed(response, "rakuten/rakuten_detail.html")

    def test_top_page_returns_200_and_expected_heading(self):
        response = self.client.get("/rakuten/%s/" % self.rakuten.id)
        self.assertContains(response, self.rakuten.title, status_code=200)


class CreateRakutenTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="secret",
        )
        self.client.force_login(self.user)

    def test_render_creation_form(self):
        response = self.client.get("/rakuten/new/")
        self.assertContains(response, "スニペットの登録", status_code=200)

    def test_create_rakuten(self):
        data = {'title': 'タイトル', 'code': 'コード', 'description': '解説'}
        self.client.post("/rakuten/new/", data)
        rakuten = Rakuten.objects.get(title='タイトル')
        self.assertEqual('コード', rakuten.code)
        self.assertEqual('解説', rakuten.description)