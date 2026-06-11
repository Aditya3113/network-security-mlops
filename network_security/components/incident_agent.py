import sys
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from network_security.exception import NetworkSecurityException
from network_security.logging import logger

class IncidentReportAgent:
    def __init__(self):
        try:
            if "OPENAI_API_KEY" not in os.environ:
                raise Exception("OPENAI_API_KEY not found in environment variables.")
            
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
            
            self.prompt = PromptTemplate(
                input_variables=["network_data"],
                template="""You are a Senior Security Operations Center (SOC) Analyst.
                Our machine learning pipeline has just flagged a network packet as a High-Risk Phishing Threat.

                Here are the extracted technical features of the malicious request (1 means presence of a trait, -1 or 0 means absence):
                {network_data}

                Draft a concise, highly professional 3-paragraph Security Incident Report. 
                Format it cleanly using Markdown. Include:
                1. Executive Summary: What happened.
                2. Technical Analysis: Highlight 2-3 specific features from the data above that look highly suspicious for phishing (e.g., unusual URL length, missing HTTPS, suspicious redirects).
                3. Remediation Actions: What the IT team should do immediately to block this threat.
                """
            )
            
            self.chain = self.prompt | self.llm | StrOutputParser()
            logger.info("Incident Report Agent initialized successfully.")
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def generate_report(self, network_data_dict: dict) -> str:
        """
        Takes a dictionary of flagged network features and returns a Markdown report.
        """
        try:
            logger.info("Generating agentic incident report for flagged threat...")
           
            formatted_data = "\n".join([f"- {k}: {v}" for k, v in network_data_dict.items()])
            
            report = self.chain.invoke({"network_data": formatted_data})
            return report
        except Exception as e:
            raise NetworkSecurityException(e, sys)