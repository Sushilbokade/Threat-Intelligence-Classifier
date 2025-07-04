from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
from .models import ThreatClassification

load_dotenv()

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

class ThreatClassifier:
    def __init__(self):
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Set up the output parser
        self.parser = PydanticOutputParser(pydantic_object=ThreatClassification)
        
        # Create the prompt template
        self.prompt = PromptTemplate(
            input_variables=["text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
            template=THREAT_CLASSIFICATION_TEMPLATE
        )
        
        # Create the chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    async def classify(self, text: str) -> ThreatClassification:
        """
        Classify the security threat level of the given text
        """
        try:
            # Generate the classification
            result = await self.chain.arun(text=text)
            # Parse the result into our Pydantic model
            classification = self.parser.parse(result)
            return classification
        except Exception as e:
            raise Exception(f"Error classifying threat: {str(e)}")