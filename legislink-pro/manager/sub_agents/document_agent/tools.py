from adk.tools import Tool
from services.google_apis import upload_to_drive
import datetime

class SaveDocumentTool(Tool):
    def __init__(self):
        super().__init__(
            name="save_document_to_drive",
            description="Guarda el contenido de un documento en una carpeta de Google Drive."
        )

    def _execute(self, document_content: str, document_type: str = "documento_legal"):
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{document_type}_{timestamp}.txt"
            
            result = upload_to_drive(file_name, document_content)
            
            if "error" in result:
                return f"Error al guardar: {result['error']}"
            
            return f"Documento guardado exitosamente en Google Drive con el nombre '{file_name}'. Link: {result.get('link')}"
        except Exception as e:
            return f"Se produjo una excepción inesperada al intentar guardar el documento: {e}" 