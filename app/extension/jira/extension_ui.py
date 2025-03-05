import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, AdminPage
from selenium_ui.jira.modules import rte_status
from selenium_ui.jira.pages.pages import Issue
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.wait_for_login_page_loaded()
    #         login_page.set_credentials(username=username, password=password)
    #         login_page.wait_for_dashboard_or_first_login_loaded()
    #         if login_page.is_first_login():
    #             login_page.first_login_setup()
    #         if login_page.is_first_login_second_page():
    #             login_page.first_login_second_page_setup()
    #         login_page.wait_for_page_loaded()
    #         # uncomment below line to do web_sudo and authorise access to admin pages
    #         # AdminPage(webdriver).go_to(password=password)
    #
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible(
                (By.ID, "ID_OF_YOUR_APP_SPECIFIC_UI_ELEMENT"))  # Wait for you app-specific UI element by ID selector

        sub_measure()

    measure()


def save_comment_with_mention(webdriver, datasets):
    issue_page = Issue(webdriver, issue_id=datasets['issue_id'])

    @print_timing("selenium_save_comment_with_mention")
    def measure():
        @print_timing("selenium_save_comment_with_mention:open_comment_form")
        def sub_measure():
            issue_page.go_to_edit_comment()  # Open edit comment page

        sub_measure()

        issue_page.fill_comment_edit_with_mention(rte_status, user_name=datasets['username'])  # Fill comment text field

        @print_timing("selenium_save_comment_with_mention:submit_form")
        def sub_measure():
            issue_page.edit_comment_submit()  # Submit comment

        sub_measure()
    measure()

