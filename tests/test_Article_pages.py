import pytest
from pages.Article_pages import PostArticlePages, URLS


class Test_Post_Article_Pages:

    @pytest.mark.parametrize("url", URLS)
    def test_author_and_last_updated(self, page, url):
        post = PostArticlePages(page)
        post.verify_author_and_last_updated(url)

    @pytest.mark.parametrize("url", URLS)
    def test_social_media_buttons(self, page, url):
        post = PostArticlePages(page)
        post.verify_social_media_buttons(url)

    @pytest.mark.parametrize("url", URLS)
    def test_hero_banner(self, page, url):
        post = PostArticlePages(page)
        post.verify_hero_banner(url)

    @pytest.mark.parametrize("url", URLS)
    def test_related_posts(self, page, url):
        post = PostArticlePages(page)
        post.verify_related_posts(url)

    @pytest.mark.parametrize("url", URLS)
    def test_post_tags(self, page, url):
        post = PostArticlePages(page)
        post.verify_post_tags(url)

    @pytest.mark.parametrize("url", URLS)
    def test_reference_section(self, page, url):
        post = PostArticlePages(page)
        post.verify_reference_section(url)