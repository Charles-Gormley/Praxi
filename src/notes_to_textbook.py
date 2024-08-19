import os
import logging
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL = "gpt-3.5-turbo"
    MAX_RETRIES = 3
    OUTPUT_FOLDER = "output"

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

class ConceptProcessor:
    @staticmethod
    def process_notes(notes: str) -> List[str]:
        """
        Process the input notes and return a list of concepts.
        """
        return [concept.strip() for concept in notes.split("\n\n") if concept.strip()]

class TextbookGenerator:
    @staticmethod
    def generate_section(concept: str) -> str:
        """
        Generate a textbook section for a given concept using the ChatGPT API.
        """
        prompt = f"""
        Create a textbook section for the following concept:

        {concept}

        Include the following elements:
        1. A clear explanation of the concept
        2. Key points or important aspects
        3. An example or analogy to illustrate the concept
        4. A brief summary

        Format the output in markdown, starting with a level 2 heading (##) for the concept title.
        Do not include any non-markdown formatting or syntax.
        """

        for attempt in range(Config.MAX_RETRIES):
            try:
                response = client.chat.completions.create(
                    model=Config.MODEL,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that creates educational content in markdown format."},
                        {"role": "user", "content": prompt}
                    ]
                )
                content = response.choices[0].message.content
                
                if not content.strip().startswith("##"):
                    content = f"## {concept}\n\n{content}"
                
                return content
            except Exception as e:
                logger.error(f"Error generating section for '{concept}': {str(e)}")
                if attempt == Config.MAX_RETRIES - 1:
                    return f"## {concept}\n\nError: Unable to generate content for this section."
        
    @classmethod
    def notes_to_textbook(cls, notes: str) -> str:
        """
        Convert notes into a structured markdown textbook.
        """
        concepts = ConceptProcessor.process_notes(notes)
        textbook_content = "# Generated Textbook\n\n"

        for i, concept in enumerate(concepts, 1):
            logger.info(f"Generating section {i} of {len(concepts)}...")
            section_content = cls.generate_section(concept)
            textbook_content += f"\n\n{section_content}"

        return textbook_content

    @staticmethod
    def generate_filename(content: str) -> str:
        """
        Generate a filename for the textbook using AI.
        """
        prompt = f"""
        Based on the following textbook content, generate a short, descriptive filename (without extension) that summarizes the main topics. 
        The filename should be in kebab-case (lowercase words separated by hyphens) and no more than 5 words long.

        Content preview:
        {content[:500]}...
        """

        try:
            response = client.chat.completions.create(
                model=Config.MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates concise filenames."},
                    {"role": "user", "content": prompt}
                ]
            )
            filename = response.choices[0].message.content.strip().lower().replace(" ", "-")
            return filename
        except Exception as e:
            logger.error(f"Error generating filename: {str(e)}")
            return "generated-textbook"

class FileHandler:
    @staticmethod
    def save_markdown(content: str) -> None:
        """
        Save the generated content as a markdown file in the output folder.
        """
        os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
        filename = TextbookGenerator.generate_filename(content)
        full_path = os.path.join(Config.OUTPUT_FOLDER, f"{filename}.md")
        
        try:
            with open(full_path, "w") as f:
                f.write(content)
            logger.info(f"Textbook saved as {full_path}")
        except IOError as e:
            logger.error(f"Error saving file: {str(e)}")

def main(notes: str) -> None:
    """
    Main execution function.
    """
    if not Config.OPENAI_API_KEY:
        logger.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return

    textbook_content = TextbookGenerator.notes_to_textbook(notes)
    FileHandler.save_markdown(textbook_content)

if __name__ == "__main__":
    # Example usage
    example_notes = """
    Python basics: variables, data types, and operators
    Control structures: if statements, loops, and functions
    Object-oriented programming: classes and inheritance
    """
    main(example_notes)
    