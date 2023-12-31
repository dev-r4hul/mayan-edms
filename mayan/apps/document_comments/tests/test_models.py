from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from .mixins import DocumentCommentTestMixin


class DocumentCommentModelTestCase(
    DocumentCommentTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_user()
        self._create_test_document_stub()

    def test_method_get_absolute_url(self):
        self._create_test_comment()

        self._clear_events()

        self.assertTrue(
            self._test_document_comment.get_absolute_url()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
