from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from typing import Any, Dict, Optional

class BaseAgent:
    """
    Clase base para todos los agentes de LegisLink Pro.
    Proporciona funcionalidad común y estructura ADK.
    """
    
    def __init__(self, name: str, description: str, instruction: str, model: str = "gemini-2.0-flash"):
        self.name = name
        self.description = description
        self.instruction = instruction
        self.model = model
        self.tools = []
        self.sub_agents = []
        
    def add_tool(self, tool):
        """Añade una herramienta al agente."""
        self.tools.append(tool)
        
    def add_sub_agent(self, sub_agent):
        """Añade un sub-agente."""
        self.sub_agents.append(sub_agent)
        
    def create_adk_agent(self):
        """Crea el agente ADK con la configuración actual."""
        return Agent(
            name=self.name,
            model=self.model,
            description=self.description,
            instruction=self.instruction,
            tools=self.tools,
            sub_agents=self.sub_agents
        )

    def update_state(self, key: str, value: Any):
        self.state[key] = value

    def get_state(self, key: str, default=None):
        return self.state.get(key, default)

    def add_to_history(self, message: Any):
        self.history.append(message)

    def get_history(self):
        return self.history 