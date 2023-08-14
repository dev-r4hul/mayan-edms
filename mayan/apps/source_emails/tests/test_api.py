from rest_framework import status

from mayan.apps.documents.events import (
    event_document_created, event_document_file_created,
    event_document_file_edited, event_document_version_created,
    event_document_version_page_created
)
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase
from mayan.apps.sources.events import event_source_created
from mayan.apps.sources.models import Source
from mayan.apps.sources.permissions import (
    permission_sources_create, permission_sources_edit
)
from mayan.apps.sources.tests.mixins.source_api_view_mixins import (
    SourceAPIViewTestMixin, SourceActionAPIViewTestMixin
)

from .mixins import (
    EmailSourceTestMixin, IMAPEmailSourceTestMixin, POP3EmailSourceTestMixin
)


class EmailSourceBackendAPIViewTestCase(
    DocumentTestMixin, SourceAPIViewTestMixin, EmailSourceTestMixin,
    BaseAPITestCase
):
    _test_source_create_auto = False
    auto_upload_test_document = True

    def test_source_create_api_view_no_permission(self):
        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Source.objects.count(), source_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_source)
        self.assertEqual(events[0].verb, event_source_created.id)


class EmailSourceBackendActionDocumentUploadAPIViewTestCase(
    DocumentTestMixin, EmailSourceTestMixin,
    SourceActionAPIViewTestMixin, BaseAPITestCase
):
    _test_source_create_auto = False
    auto_upload_test_document = False

    def test_basic_no_permission(self):
        self._test_source_create()

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_source_action_execute_post_api_view(
            action_name='document_upload'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.objects.count(), test_document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_basic_with_access(self):
        self._silence_logger(name='mayan.apps.converter.backends')

        self._test_source_create()

        self.grant_access(
            obj=self._test_source, permission=permission_sources_edit
        )

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_source_action_execute_post_api_view(
            action_name='document_upload'
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(Document.objects.count(), test_document_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 3)

        test_document = Document.objects.first()
        test_document_file = test_document.file_latest
        test_document_version = test_document.version_active

        self.assertEqual(events[0].action_object, self._test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_created.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_version)
        self.assertEqual(events[2].verb, event_document_version_created.id)


class IMAPEmailSourceBackendAPIViewTestCase(
    DocumentTestMixin, SourceAPIViewTestMixin, IMAPEmailSourceTestMixin,
    BaseAPITestCase
):
    _test_source_create_auto = False
    auto_upload_test_document = True

    def test_source_create_api_view_no_permission(self):
        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Source.objects.count(), source_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_source)
        self.assertEqual(events[0].verb, event_source_created.id)


class IMAPEmailSourceBackendActionDocumentUploadAPIViewTestCase(
    DocumentTestMixin, IMAPEmailSourceTestMixin,
    SourceActionAPIViewTestMixin, BaseAPITestCase
):
    _test_source_create_auto = False
    auto_upload_test_document = False

    def test_basic_no_permission(self):
        self._test_source_create()

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_source_action_execute_post_api_view(
            action_name='document_upload'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.objects.count(), test_document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_basic_with_access(self):
        self._silence_logger(name='mayan.apps.converter.backends')

        self._test_source_create()

        self.grant_access(
            obj=self._test_source, permission=permission_sources_edit
        )

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_source_action_execute_post_api_view(
            action_name='document_upload'
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(Document.objects.count(), test_document_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 5)

        test_document = Document.objects.first()
        test_document_file = test_document.file_latest
        test_document_version = test_document.version_active
        test_document_version_page = test_document_version.pages.first()

        self.assertEqual(events[0].action_object, self._test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_created.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_file)
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        self.assertEqual(events[3].action_object, test_document)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_version)
        self.assertEqual(events[3].verb, event_document_version_created.id)

        self.assertEqual(events[4].action_object, test_document_version)
        self.assertEqual(events[4].actor, self._test_case_user)
        self.assertEqual(events[4].target, test_document_version_page)
        self.assertEqual(
            events[4].verb, event_document_version_page_created.id
        )


class POP3EmailSourceBackendAPIViewTestCase(
    DocumentTestMixin, SourceAPIViewTestMixin, POP3EmailSourceTestMixin,
    BaseAPITestCase
):
    _test_source_create_auto = False
    auto_upload_test_document = True

    def test_source_create_api_view_no_permission(self):
        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Source.objects.count(), source_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_source_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_sources_create)

        source_count = Source.objects.count()

        self._clear_events()

        response = self._request_test_source_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Source.objects.count(), source_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_source)
        self.assertEqual(events[0].verb, event_source_created.id)


class POP3EmailSourceBackendActionDocumentUploadAPIViewTestCase(
    DocumentTestMixin, POP3EmailSourceTestMixin,
    SourceActionAPIViewTestMixin, BaseAPITestCase
):
    _test_source_create_auto = False
    auto_upload_test_document = False

    def test_basic_no_permission(self):
        self._test_source_create()

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_source_action_execute_post_api_view(
            action_name='document_upload'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Document.objects.count(), test_document_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_basic_with_access(self):
        self._silence_logger(name='mayan.apps.converter.backends')

        self._test_source_create()

        self.grant_access(
            obj=self._test_source, permission=permission_sources_edit
        )

        test_document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_source_action_execute_post_api_view(
            action_name='document_upload'
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(Document.objects.count(), test_document_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 5)

        test_document = Document.objects.first()
        test_document_file = test_document.file_latest
        test_document_version = test_document.version_active
        test_document_version_page = test_document_version.pages.first()

        self.assertEqual(events[0].action_object, self._test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

        self.assertEqual(events[1].action_object, test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, test_document_file)
        self.assertEqual(events[1].verb, event_document_file_created.id)

        self.assertEqual(events[2].action_object, test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_file)
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        self.assertEqual(events[3].action_object, test_document)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_version)
        self.assertEqual(events[3].verb, event_document_version_created.id)

        self.assertEqual(events[4].action_object, test_document_version)
        self.assertEqual(events[4].actor, self._test_case_user)
        self.assertEqual(events[4].target, test_document_version_page)
        self.assertEqual(
            events[4].verb, event_document_version_page_created.id
        )