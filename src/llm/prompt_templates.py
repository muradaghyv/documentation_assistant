from string import Template

class PromptTemplates:
    ANSWER_TEMPLATE = Template("""
    Based on the following context, please answer the question. If you cannot answer the question based on the context alone, say so.

    Context:
    $context

    Question: $question

    Please provide a clear and concise answer, using only the information from the context above.
""")
    
    SYSTEM_PROMPT = """You are a helpful AI assistant specialized in Python and Django documentation. 
    Your responses should be:
    1. Accurate and based solely on the provided context
    2. Clear and concise
    3. Include code examples when relevant
    4. Mention if information is incomplete or unclear
"""

    @classmethod
    def create_prompt(cls, context: str, question: str) -> str:
        """Creating a formatting prompt from a context and a question."""
        cls.ANSWER_TEMPLATE.substitute(
            context=context, question=question
        )