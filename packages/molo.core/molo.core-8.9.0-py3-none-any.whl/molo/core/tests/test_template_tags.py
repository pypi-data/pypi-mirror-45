# coding=utf-8
import pytest
from django.test import TestCase, RequestFactory
from mock import patch
from molo.core.models import (
    Main, SiteLanguageRelation, Languages, BannerPage, ArticlePageTags,
    FormPage)
from molo.core.tests.base import MoloTestCaseMixin
from molo.core.templatetags.core_tags import (
    get_parent, bannerpages, load_tags_for_article, get_recommended_articles,
    hero_article, render_translations
)
from molo.core.templatetags.forms_tags import forms_list


@pytest.mark.django_db
class TestModels(TestCase, MoloTestCaseMixin):

    def setUp(self):
        self.mk_main()
        self.main = Main.objects.all().first()
        self.factory = RequestFactory()
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

        self.yourmind = self.mk_section(
            self.section_index, title='Your mind')
        self.yourmind_sub = self.mk_section(
            self.yourmind, title='Your mind subsection')
        # create a requset object
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.site = self.site

    def create_form_page(
            self, parent, title="Test Form",
            slug="test-form", **kwargs):
        form_page = FormPage(
            title=title,
            slug=slug,
            intro='Introduction to Test Form ...',
            thank_you_text='Thank you for taking the Test Form',
            **kwargs
        )
        parent.add_child(instance=form_page)
        form_page.save_revision().publish()
        return form_page

    def test_get_form_list_homepage(self):
        context = {
            'locale_code': 'en',
            'request': self.request,
            'forms': self.create_form_page(self.form_index)
        }
        context = forms_list(context)
        self.assertEqual(len(context['forms']), 1)

    def test_render_translations(self):
        # this should return an empty dictionary for non main lang pages
        article = self.mk_articles(self.yourmind, 1)[0]
        fr_article = self.mk_article_translation(article, self.french)
        self.assertEquals(render_translations({}, fr_article), {})

    def test_bannerpages_without_position(self):
        banner = BannerPage(title='test banner')
        self.banner_index.add_child(instance=banner)
        banner.save_revision().publish()
        banner2 = BannerPage(title='test banner 2')
        self.banner_index.add_child(instance=banner2)
        banner2.save_revision().publish()
        banner3 = BannerPage(title='test banner 3')
        self.banner_index.add_child(instance=banner3)
        banner3.save_revision().publish()
        self.assertEqual(self.main.bannerpages().count(), 3)

        request = self.factory.get('/')
        request.site = self.site

        self.assertEquals(len(bannerpages({
            'locale_code': 'en', 'request': request})['bannerpages']), 3)

    def test_bannerpages_with_position(self):
        banner = BannerPage(title='test banner')
        self.banner_index.add_child(instance=banner)
        banner.save_revision().publish()
        banner2 = BannerPage(title='test banner 2')
        self.banner_index.add_child(instance=banner2)
        banner2.save_revision().publish()
        banner3 = BannerPage(title='test banner 3')
        self.banner_index.add_child(instance=banner3)
        banner3.save_revision().publish()
        self.assertEqual(self.main.bannerpages().count(), 3)

        request = self.factory.get('/')
        request.site = self.site

        self.assertEquals(len(bannerpages({
            'locale_code': 'en',
            'request': request}, position=0)['bannerpages']), 1)
        self.assertEquals(bannerpages({
            'locale_code': 'en',
            'request': request}, position=0)['bannerpages'][0].title,
            'test banner')
        self.assertEquals(bannerpages({
            'locale_code': 'en',
            'request': request}, position=1)['bannerpages'][0].title,
            'test banner 2')

    def test_bannerpages_with_position_out_of_range(self):
        banner = BannerPage(title='test banner')
        self.banner_index.add_child(instance=banner)
        banner.save_revision().publish()
        banner2 = BannerPage(title='test banner 2')
        self.banner_index.add_child(instance=banner2)
        banner2.save_revision().publish()
        banner3 = BannerPage(title='test banner 3')
        self.banner_index.add_child(instance=banner3)
        banner3.save_revision().publish()
        self.assertEqual(self.main.bannerpages().count(), 3)

        request = self.factory.get('/')
        request.site = self.site

        self.assertEquals(bannerpages({
            'locale_code': 'en',
            'request': request}, position=4), None)

    def test_get_parent_template_tag(self):
        request = self.factory.get('/')
        request.site = self.site

        article = self.mk_articles(self.yourmind, 1)[0]
        fr_article = self.mk_article_translation(article, self.french)

        self.assertEquals(
            get_parent({'locale_code': 'fr', 'request': request}, article),
            self.yourmind)
        self.assertEquals(
            get_parent({'locale_code': 'fr', 'request': request}, fr_article),
            self.yourmind)
        self.assertEquals(get_parent(
            {'locale_code': 'fr', 'request': request}, self.yourmind_sub),
            self.yourmind)

        fr_yourmind = self.mk_section_translation(self.yourmind, self.french)
        self.assertEquals(
            get_parent({'locale_code': 'en', 'request': request}, article),
            self.yourmind)
        self.assertEquals(
            get_parent({'locale_code': 'en', 'request': request}, fr_article),
            self.yourmind)
        self.assertEquals(get_parent(
            {'locale_code': 'en', 'request': request}, self.yourmind_sub),
            self.yourmind)

        self.assertEquals(
            get_parent({'locale_code': 'fr', 'request': request}, article),
            fr_yourmind)
        self.assertEquals(
            get_parent({'locale_code': 'fr', 'request': request}, fr_article),
            fr_yourmind)
        self.assertEquals(get_parent(
            {'locale_code': 'fr', 'request': request}, self.yourmind_sub),
            fr_yourmind)

        self.assertEquals(get_parent(
            {'locale_code': 'fr', 'request': request}, self.yourmind),
            None)

    def test_load_tags_for_article(self):
        request = self.factory.get('/')
        request.site = self.site
        article1 = self.mk_article(self.yourmind, title='article 1')

        tag = self.mk_tag(parent=self.tag_index)
        ArticlePageTags.objects.create(page=article1, tag=tag)
        self.assertEquals(load_tags_for_article(
            {
                'locale_code': 'en',
                'request': request
            }, article1)[0],
            tag)
        self.assertEquals(load_tags_for_article(
            {
                'locale_code': 'en',
                'request': request
            }, self.yourmind),
            None)

    def test_get_recommended_articles(self):
        request = self.factory.get('/')
        request.site = self.site
        article1 = self.mk_article(self.yourmind, title='article 1')

        self.assertEquals(get_recommended_articles(
            {'locale_code': 'en', 'request': request}, article1),
            [])

    @patch('molo.core.templatetags.core_tags.get_pages')
    def test_hero_article_empty_queryset_if_no_site(self, get_pages_mock):
        request = self.factory.get('/')
        request.site = None
        context = {'request': request, 'locale_code': 'en'}
        get_pages_mock.return_value = []

        self.assertEquals(
            hero_article(context),
            {
                'articles': [],
                'request': request,
                'locale_code': 'en',
            }
        )
