import io
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from config.settings import settings
from google.cloud import aiplatform

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/calendar'
]

def _get_google_service(service_name, version):
    """Función genérica para obtener un servicio de Google API."""
    try:
        credentials_path = settings.GOOGLE_APPLICATION_CREDENTIALS
        if not credentials_path or not os.path.exists(credentials_path):
            print(f"Error: El archivo de credenciales de Google no se encuentra en la ruta: {credentials_path}")
            return None

        creds = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=SCOPES)
        service = build(service_name, version, credentials=creds)
        return service
    except Exception as e:
        print(f"Error al autenticar con Google API ({service_name}): {e}")
        return None

def get_drive_service():
    """Autentica y devuelve un objeto de servicio de Google Drive."""
    return _get_google_service('drive', 'v3')

def get_calendar_service():
    """Autentica y devuelve un objeto de servicio de Google Calendar."""
    return _get_google_service('calendar', 'v3')

def upload_to_drive(file_name: str, file_content: str, mimetype: str = 'text/plain'):
    """Sube un archivo a la carpeta especificada en Google Drive."""
    service = get_drive_service()
    if not service:
        return {"error": "No se pudo conectar con Google Drive."}
    
    folder_id = settings.GOOGLE_DRIVE_FOLDER_ID
    if not folder_id:
        return {"error": "El ID de la carpeta de Google Drive no está configurado."}
        
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    
    fh = io.BytesIO(file_content.encode('utf-8'))
    media = MediaIoBaseUpload(fh, mimetype=mimetype, resumable=True)
    
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        return {"id": file.get('id'), "link": file.get('webViewLink')}
    except Exception as e:
        print(f"Error al subir el archivo a Google Drive: {e}")
        return {"error": "Ocurrió un error durante la subida del archivo."}

def create_calendar_event(summary: str, start_time: str, end_time: str, attendees: list = None):
    """Crea un evento en Google Calendar."""
    service = get_calendar_service()
    if not service:
        return {"error": "No se pudo conectar con Google Calendar."}
        
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'America/Santiago'},
        'end': {'dateTime': end_time, 'timeZone': 'America/Santiago'},
        'attendees': [{'email': email} for email in attendees] if attendees else [],
    }
    
    try:
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return {'id': created_event.get('id'), 'link': created_event.get('htmlLink')}
    except Exception as e:
        print(f"Error al crear el evento de calendario: {e}")
        return {"error": "Ocurrió un error al crear el evento."}

# --- Vertex AI Search (Matching Engine) Functions ---

def get_vertex_ai_client():
    """Inicializa y devuelve el cliente de Vertex AI."""
    try:
        aiplatform.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)
        return aiplatform
    except Exception as e:
        print(f"Error al inicializar Vertex AI: {e}")
        return None

def create_vector_search_index(display_name: str, contents_delta_uri: str, embedding_dimensions: int):
    """Crea un nuevo índice de Vector Search."""
    aiplatform = get_vertex_ai_client()
    if not aiplatform:
        return None
    try:
        index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
            display_name=display_name,
            contents_delta_uri=contents_delta_uri,
            dimensions=embedding_dimensions,
            approximate_neighbors_count=150,
            distance_measure_type="DOT_PRODUCT_DISTANCE",
            leaf_node_embedding_count=500,
            leaf_nodes_to_search_percent=7,
        )
        return index
    except Exception as e:
        print(f"Error al crear el índice de Vector Search: {e}")
        return None

def upsert_to_index(index_id: str, datapoints: list):
    """Inserta o actualiza vectores de datos en un índice existente."""
    aiplatform = get_vertex_ai_client()
    if not aiplatform:
        return {"error": "No se pudo inicializar Vertex AI."}
    try:
        index = aiplatform.MatchingEngineIndex(index_name=index_id)
        index.upsert_datapoints(datapoints=datapoints)
        return {"status": "success"}
    except Exception as e:
        print(f"Error al hacer upsert en el índice: {e}")
        return {"error": str(e)}

def query_vector_search(index_endpoint_id: str, query_embedding: list, num_neighbors: int = 5):
    """Realiza una búsqueda de vecinos más cercanos en un endpoint de índice."""
    aiplatform = get_vertex_ai_client()
    if not aiplatform:
        return {"error": "No se pudo inicializar Vertex AI."}
    try:
        index_endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=index_endpoint_id)
        response = index_endpoint.find_neighbors(
            queries=[query_embedding],
            num_neighbors=num_neighbors
        )
        return response
    except Exception as e:
        print(f"Error al consultar Vector Search: {e}")
        return {"error": str(e)}
