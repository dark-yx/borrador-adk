#!/usr/bin/env python3
"""
Script para configurar Vertex AI Search para LegisLink Pro
"""

import os
import sys
from google.cloud import aiplatform
from google.cloud.aiplatform import MatchingEngineIndex, MatchingEngineIndexEndpoint

def setup_vertex_ai():
    """Configura Vertex AI Search para el proyecto"""
    
    # Configuración del proyecto
    PROJECT_ID = "legislink-pro"
    LOCATION = "us-central1"
    
    # Inicializar Vertex AI
    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    
    print("🚀 Configurando Vertex AI Search para LegisLink Pro...")
    
    try:
        # Crear índice de búsqueda vectorial
        index = MatchingEngineIndex.create_tree_ah_index(
            display_name="legislink-legal-docs",
            contents_delta_uri="gs://legislink-docs/embeddings/",
            dimensions=768,  # Dimensiones del modelo de embedding
            approximate_neighbors_count=150,
            distance_measure_type="DOT_PRODUCT_DISTANCE",
            leaf_node_embedding_count=500,
            leaf_nodes_to_search_percent=7,
        )
        
        print(f"✅ Índice creado: {index.name}")
        
        # Crear endpoint para el índice
        endpoint = MatchingEngineIndexEndpoint.create(
            display_name="legislink-search-endpoint",
            network="projects/legislink-pro/global/networks/default",
        )
        
        print(f"✅ Endpoint creado: {endpoint.name}")
        
        # Desplegar el índice al endpoint
        deployed_index = endpoint.deploy_index(
            index=index,
            deployed_index_id="legislink-legal-docs-deployed"
        )
        
        print(f"✅ Índice desplegado: {deployed_index.name}")
        
        # Guardar información en un archivo de configuración
        config = {
            "index_id": index.name,
            "endpoint_id": endpoint.name,
            "deployed_index_id": deployed_index.name
        }
        
        with open("vertex_ai_config.json", "w") as f:
            import json
            json.dump(config, f, indent=2)
        
        print("✅ Configuración guardada en vertex_ai_config.json")
        
        return config
        
    except Exception as e:
        print(f"❌ Error configurando Vertex AI: {e}")
        return None

if __name__ == "__main__":
    setup_vertex_ai()
