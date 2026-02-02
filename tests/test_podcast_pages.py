from pages.podcast_pages import PodcastPages

class TestPodcastPages:
    def test_podcast_pages(self, page):
        podcast = PodcastPages(page)
        podcast.verify_all_pages()
