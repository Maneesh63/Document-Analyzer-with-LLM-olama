from rag.models import Document
from rag.pipeline import HandleLLM
from django.shortcuts import get_object_or_404
from rag.models import QueryHistory

class DocumentUploadHandler:

    def __init__(self, file):
        self.file = file

    def upload_and_embed(self):

        if not self.file:
            return "No file provided", None

        if not self.file.name.endswith('.pdf'):
            return "Unsupported file type. Only PDF files are allowed.", None

        document = Document.objects.create(
            file=self.file,
            file_name=self.file.name,
            status=Document.processing
        )

        try:

            error, embed_file = HandleLLM.index_pdf(
                document.file.path,
                document.document_id
            )

            if embed_file:

                document.status = Document.ready
                document.total_chunks = embed_file
                document.file_path= document.file.path        
                document.save()

                return None, document

            return error, None

        except Exception as e:
            document.status = Document.failed
            document.save()

            return str(e), None
        

class DocumentOperationHandler:
    
    def __init__(self, question, document_id):
        self.document_id = document_id
        self.question = question

    def query_document(self):
        document = get_object_or_404(Document, document_id=self.document_id)
        print("document_id =============>",self.document_id)
        print("question ================>", self.question)
        if document.status != Document.ready:
           return "Document not ready yet", None
        
        error, result = HandleLLM.query_document(self.question, self.document_id)
        if error: 
            return "Error querying the document", None
        
        try:
            QueryHistory.objects.create(
                document=document,
                question=self.question,
                answer=result["answer"]
            )

            return None, {
                "question": self.question,
                "answer": result['answer'],
                # "source_chunks": result['source_chunks']
            }
        
        except Exception as e:
            return str(e), None

        

        

