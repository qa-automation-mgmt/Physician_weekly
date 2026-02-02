from pages.E2E_work_flow import E2EFlowPage

class TestE2EFlow:
    def test_search_functionality(self, page):
        search = E2EFlowPage(page)
        search.search_function()
