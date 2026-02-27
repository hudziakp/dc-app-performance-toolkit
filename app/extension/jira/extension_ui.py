import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.modules import rte_status
from selenium_ui.jira.pages.pages import Issue
from selenium_ui.jira.pages.pages import Login, AdminPage
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    issue_page = Issue(webdriver, issue_id=datasets['current_session']['issue_id'])

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            issue_page.go_to_edit_comment()  # Open edit comment page
        sub_measure()
    measure()

def save_comment_with_mention(webdriver, datasets):
    user_name = random.choice(datasets['current_session']['username'])
    issue_page = Issue(webdriver, issue_id=datasets['current_session']['issue_id'])

    @print_timing("selenium_save_comment_with_mention")
    def measure():
        @print_timing("selenium_save_comment_with_mention:open_comment_form")
        def sub_measure():
            issue_page.go_to_edit_comment()  # Open edit comment page

        sub_measure()

        issue_page.fill_comment_edit_with_mention(rte_status, user_name)  # Fill comment text field

        @print_timing("selenium_save_comment_with_mention:submit_form")
        def sub_measure():
            issue_page.edit_comment_submit()  # Submit comment

        sub_measure()
    measure()

