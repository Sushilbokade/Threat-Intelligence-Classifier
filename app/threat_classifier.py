from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
from .models import ThreatClassification

load_dotenv()

# Original general security template
THREAT_CLASSIFICATION_TEMPLATE = """
Analyze the following log/text data for potential security threats:

{text}

Classify the threat level as one of: LOW, MEDIUM, HIGH, CRITICAL
Consider the following factors:
- Unauthorized access attempts
- Suspicious IP addresses or domains
- Malware indicators
- Data exfiltration attempts
- Protocol anomalies
- Known attack patterns
- System modification attempts
- Privilege escalation indicators

Provide a detailed explanation of why this threat level was assigned.
{format_instructions}
"""

# Web application security template
WEB_SECURITY_TEMPLATE = """
Analyze the following web application log/request data for security threats:

{text}

Classify the threat level as one of: LOW, MEDIUM, HIGH, CRITICAL
Consider these web-specific factors:
- SQL Injection attempts
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- File upload attempts
- Authentication bypass attempts
- Path traversal
- API abuse patterns
- Session manipulation
- Known web vulnerabilities
- Unauthorized access to sensitive endpoints

Provide a detailed explanation of why this threat level was assigned.
{format_instructions}
"""

class ThreatClassifier:
    def __init__(self, security_focus="general"):
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Set up the output parser
        self.parser = PydanticOutputParser(pydantic_object=ThreatClassification)
        
        # Select template based on security focus
        template = WEB_SECURITY_TEMPLATE if security_focus == "web" else THREAT_CLASSIFICATION_TEMPLATE
        
        # Create the prompt template
        self.prompt = PromptTemplate(
            input_variables=["text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
            template=template
        )
        
        # Create the chain using the new RunnableSequence syntax
        self.chain = (
            {"text": RunnablePassthrough()} 
            | self.prompt 
            | self.llm 
            | self.parser
        )
    
    async def classify(self, text: str) -> ThreatClassification:
        """
        Classify the security threat level of the given text
        """
        try:
            # Generate the classification using the new invoke syntax
            classification = await self.chain.ainvoke(text)
            return classification
        except Exception as e:
            raise Exception(f"Error classifying threat: {str(e)}")