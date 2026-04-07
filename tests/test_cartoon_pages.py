from pages.cartoon_pages import CartoonPage

class TetCartoonPages:
    def test_cartoon_pages(self, page):
        cartoon = CartoonPage(page)
        cartoon.verify_all_pages()
