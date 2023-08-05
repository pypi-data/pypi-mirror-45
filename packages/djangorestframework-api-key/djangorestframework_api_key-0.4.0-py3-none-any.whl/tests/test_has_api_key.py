import pytest
from rest_framework import generics, permissions
from rest_framework.response import Response

from rest_framework_api_key.permissions import HasAPIKey

pytestmark = pytest.mark.django_db


@pytest.fixture(name="view")
def fixture_view(view_with_permissions):
    return view_with_permissions(HasAPIKey)


def test_if_no_token_then_permission_denied(create_request, view):
    request = create_request(token=None, secret_key="1234")
    response = view(request)
    assert response.status_code == 403


def test_if_no_secret_key_then_permission_denied(create_request, view):
    request = create_request(token="abc", secret_key=None)
    response = view(request)
    assert response.status_code == 403


def test_if_no_api_key_for_token_then_permission_denied(create_request, view):
    # No API key in database, so token won't be found.
    request = create_request(token="abc", secret_key="1234")
    response = view(request)
    assert response.status_code == 403


def test_if_revoked_then_permission_denied(
    create_request, create_api_key, view
):
    key = create_api_key(secret_key="foo", revoked=True)
    request = create_request(token=key.token, secret_key="bar")
    response = view(request)
    assert response.status_code == 403


def test_if_valid_token_and_secret_key_then_permission_granted(
    create_request, create_api_key, view
):
    key = create_api_key(secret_key="foo")
    request = create_request(token=key.token, secret_key="foo")
    response = view(request)
    assert response.status_code == 200


def test_object_permission(create_request):
    class DenyObject(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            return False

    class View(generics.GenericAPIView):
        permission_classes = [HasAPIKey | DenyObject]

        def get(self, request):
            self.check_object_permissions(request, object())
            return Response()

    view = View.as_view()

    # NOTE: no API key passed => permission checks should fail
    request = create_request()
    response = view(request)
    assert response.status_code == 403
