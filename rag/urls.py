from django.urls import path
from rag.views import UploadDocumentView, QueryDocumentView


urlpatterns = [
    path("upload_file/", UploadDocumentView.as_view(), name="upload_file"),

    path("query_document/", QueryDocumentView.as_view(), name="query_document")
]