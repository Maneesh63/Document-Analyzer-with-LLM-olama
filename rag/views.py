from django.shortcuts import render
from rest_framework.views import APIView
from rag.handlers import DocumentUploadHandler, DocumentOperationHandler
from rest_framework.response import Response
from rest_framework import status
 
class UploadDocumentView(APIView):
    def post(self, request):
        
        file = request.FILES.get('file')
        handle_file = DocumentUploadHandler(file)
        error, document = handle_file.upload_and_embed()
        if error:
            return Response(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {
                "message": "File uploaded successfully",
                "document_id": str(document.document_id),
                "file_name": document.file_name,
                "status": document.status,
                "total_chunks": document.total_chunks
            },
            status=status.HTTP_200_OK
        )
    

class QueryDocumentView(APIView):

    def post(self, request):

        document_id = request.data.get("document_id")
        question = request.data.get("question")

        handler = DocumentOperationHandler(question, document_id)

        error, result = handler.query_document()

        if error:
            return Response(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            result,
            status=status.HTTP_200_OK
        )