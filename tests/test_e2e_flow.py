from pages.E2E_work_flow import E2EFlowPage

class TestE2EFlow:
    def test_e2e_flow_In_user_search_journey(self, page):
        search = E2EFlowPage(page)
        search.search_function()
