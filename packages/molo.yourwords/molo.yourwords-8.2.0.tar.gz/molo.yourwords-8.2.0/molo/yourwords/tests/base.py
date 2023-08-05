from django.test import TestCase, Client
from django.contrib.auth.models import User

from molo.core.tests.base import MoloTestCaseMixin
from molo.core.models import (
    SiteLanguageRelation,
    Languages,
    Main
)

from molo.yourwords.models import YourWordsCompetitionIndexPage


class BaseYourWordsTestCase(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.mk_main()
        self.language_setting = Languages.objects.create(
            site_id=self.main.get_site().pk)
        self.english = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting,
            locale='en',
            is_active=True)
        self.french = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting,
            locale='fr',
            is_active=True)
        self.user = self.login()

        # Create competition index page
        self.competition_index = (YourWordsCompetitionIndexPage
                                  .objects.child_of(self.main).first())

        self.superuser_name = 'test_superuser'
        self.superuser_password = 'password'
        self.superuser = User.objects.create_superuser(
            username=self.superuser_name,
            email='admin@example.com',
            password=self.superuser_password,
            is_staff=True)
        self.client = Client()

        self.mk_main2()
        self.main2 = Main.objects.all().last()
        self.language_setting2 = Languages.objects.create(
            site_id=self.main2.get_site().pk)
        self.english2 = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting2,
            locale='en',
            is_active=True)
        self.french2 = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting2,
            locale='fr',
            is_active=True)

        self.competition_index_main2 = (YourWordsCompetitionIndexPage
                                        .objects.child_of(self.main2).first())

        self.client2 = Client(HTTP_HOST=self.main2.get_site().hostname)
