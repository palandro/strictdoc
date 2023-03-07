from seleniumbase import BaseCase

from tests.end2end.end2end_test_setup import End2EndTestSetup
from tests.end2end.helpers.constants import NODE_1
from tests.end2end.helpers.screens.document.form_edit_requirement import (
    Form_EditRequirement,
)
from tests.end2end.helpers.screens.document_tree.screen_document_tree import (
    Screen_DocumentTree,
)
from tests.end2end.server import SDocTestServer


class Test_UC07_G1_T03_RemoveLink(BaseCase):
    def test_01(self):
        test_setup = End2EndTestSetup(path_to_test_file=__file__)

        with SDocTestServer(
            input_path=test_setup.path_to_sandbox
        ) as test_server:
            self.open(test_server.get_host_and_port())

            screen_document_tree = Screen_DocumentTree(self)

            screen_document_tree.assert_on_screen()
            screen_document_tree.assert_contains_string("Document 1")

            screen_document = screen_document_tree.do_click_on_first_document()

            screen_document.assert_on_screen()
            screen_document.assert_is_document_title("Document 1")

            screen_document.assert_text("Hello world!")

            requirement1_order = NODE_1
            requirement2_order = NODE_1 + 1

            # Make sure there is the reference to the child in Requirement 1:
            screen_document.assert_requirement_uid_contains(
                "REQ-001", requirement1_order
            )
            screen_document.assert_requirement_has_child_link(
                "REQ-002", requirement1_order
            )
            # Make sure there is the reference to the parent in Requirement 2:
            screen_document.assert_requirement_uid_contains(
                "REQ-002", requirement2_order
            )
            screen_document.assert_requirement_has_parent_link(
                "REQ-001", requirement2_order
            )

            # edit the second requirement
            form_edit_requirement: Form_EditRequirement = (
                screen_document.do_open_form_edit_requirement(
                    requirement2_order
                )
            )
            form_edit_requirement.do_delete_parent_link()
            # Make sure that the field is removed from the form:
            form_edit_requirement.assert_form_has_no_parents()
            form_edit_requirement.do_form_submit()

            # Make sure there is no reference to the child in Requirement 1:
            screen_document.assert_requirement_uid_contains(
                "REQ-001", requirement1_order
            )
            screen_document.assert_requirement_has_not_child_link(
                "REQ-002", requirement1_order
            )
            # Make sure there is no reference to the parent in Requirement 2:
            screen_document.assert_requirement_uid_contains(
                "REQ-002", requirement2_order
            )
            screen_document.assert_requirement_has_not_parent_link(
                "REQ-001", requirement2_order
            )

        assert test_setup.compare_sandbox_and_expected_output()
