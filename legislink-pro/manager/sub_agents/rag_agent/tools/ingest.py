import os
import json
import google.generativeai as genai
from config.settings import settings
from services.google_apis import upsert_to_index
import hashlib

# Configure the generative AI model for embeddings
genai.configure(api_key=settings.GEMINI_API_KEY)

def simple_chunker(text, chunk_size=500, chunk_overlap=50):
    """Divide un texto en fragmentos (chunks) con superposición."""
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def ingest_documents_to_vertex(directory_path: str, index_id: str):
    """
    Ingesta documentos, genera embeddings y los sube a un índice de Vertex AI.
    """
    print(f"Iniciando ingesta desde el directorio: {directory_path} hacia el índice de Vertex AI: {index_id}")
    
    if not os.path.isdir(directory_path):
        print(f"Error: El directorio '{directory_path}' no existe.")
        return {"status": "error", "message": "Directorio no encontrado"}

    files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
    if not files:
        print("No se encontraron documentos .txt para ingestar.")
        return {"status": "ok", "message": "No se encontraron documentos .txt"}

    print(f"Archivos .txt encontrados: {', '.join(files)}")
    
    datapoints_to_upsert = []
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chunks = simple_chunker(content)
        print(f"Procesando y generando embeddings para {len(chunks)} chunks de '{file_name}'...")

        for i, chunk in enumerate(chunks):
            try:
                # Generar embedding para el chunk
                result = genai.embed_content(
                    model="models/text-embedding-004", # Modelo de embedding de Gemini
                    content=chunk,
                    task_type="RETRIEVAL_DOCUMENT"
                )
                embedding = result['embedding']
                
                # Crear un ID único para el datapoint
                datapoint_id = hashlib.sha256(f"{file_name}-{i}".encode()).hexdigest()
                
                datapoints_to_upsert.append({
                    "datapoint_id": datapoint_id,
                    "feature_vector": embedding,
                    # Se pueden agregar restricciones/metadatos aquí si es necesario
                    # "restricts": [{"namespace": "source", "allow_list": [file_name]}]
                })
            except Exception as e:
                print(f"Error generando embedding para el chunk {i} de {file_name}: {e}")

    # Subir los datapoints al índice de Vertex AI
    if datapoints_to_upsert:
        print(f"Subiendo {len(datapoints_to_upsert)} vectores al índice de Vertex AI...")
        upsert_result = upsert_to_index(index_id=index_id, datapoints=datapoints_to_upsert)
        if "error" in upsert_result:
            print(f"Error durante el upsert a Vertex AI: {upsert_result['error']}")
            return {"status": "error", "message": upsert_result['error']}
    else:
        print("No se generaron vectores para subir.")
        return {"status": "ok", "message": "No se generaron vectores"}


    print(f"Ingesta a Vertex AI completada.")
    return {
        "status": "success",
        "files_processed": len(files),
        "vectors_generated": len(datapoints_to_upsert)
    }

if __name__ == '__main__':
    # Esto es un ejemplo. El INDEX_ID debe existir en Vertex AI.
    VERTEX_AI_INDEX_ID = os.getenv("VERTEX_AI_INDEX_ID", "tu-index-id") # Reemplazar con tu ID de índice real
    
    sample_docs_path = 'sample_legal_docs'
    os.makedirs(sample_docs_path, exist_ok=True)
    with open(os.path.join(sample_docs_path, 'ley_01.txt'), 'w', encoding='utf-8') as f:
        f.write("Artículo 1: Todo ciudadano tiene derecho a la libre expresión. Este derecho incluye la libertad de buscar, recibir y difundir informaciones e ideas de toda índole, sin consideración de fronteras, ya sea oralmente, por escrito o en forma impresa o artística, o por cualquier otro procedimiento de su elección.")
    with open(os.path.join(sample_docs_path, 'ley_02.txt'), 'w', encoding='utf-8') as f:
        f.write("Artículo 2: La ley protegerá la honra y la intimidad personal y familiar. Nadie podrá ser objeto de injerencias arbitrarias o abusivas en su vida privada, en la de su familia, en su domicilio o en su correspondencia, ni de ataques ilegales a su honra o reputación.")
        
    ingest_documents_to_vertex(sample_docs_path, VERTEX_AI_INDEX_ID) 