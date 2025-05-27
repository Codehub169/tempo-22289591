import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape, exceptions as jinja_exceptions
import os
from typing import Dict, Any

def generate_portfolio_html(data: Dict[str, Any], template_name: str = "generated_portfolio_template.html") -> str:
    """
    Generates portfolio HTML content using Jinja2 templating.

    Args:
        data (dict): The structured data extracted from the resume.
                     This dictionary should contain keys like 'name', 'title', 'email',
                     'phone', 'linkedin', 'github', 'website', 'summary', 'experience',
                     'education', 'skills', 'projects', and 'profile_image_url'.
        template_name (str): The name of the template file located in the 'templates' directory.
                             Defaults to "generated_portfolio_template.html".

    Returns:
        str: The rendered HTML content as a string.
             Returns an error message string if the template is not found or rendering failed.
    """
    # Determine the absolute path to the templates directory
    # __file__ is backend/core/portfolio_generator.py
    # os.path.dirname(__file__) is backend/core/
    # os.path.join(..., '..', 'templates') is backend/templates/
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True, # Removes the first newline after a block
        lstrip_blocks=True # Strips leading whitespace from a block
    )
    
    try:
        template = env.get_template(template_name)
        current_year = datetime.datetime.now().year
        # The template expects the data to be passed as 'data' and 'current_year'.
        return template.render(data=data, current_year=current_year)
    except jinja_exceptions.TemplateNotFound:
        print(f"Error: Template '{template_name}' not found in directory '{template_dir}'.")
        return f"<p>Error: Could not generate portfolio. Template '{template_name}' not found.</p>"
    except Exception as e:
        # Handle other rendering errors
        print(f"Error rendering template {template_name}: {e}")
        return f"<p>Error: Could not generate portfolio. Template '{template_name}' rendering failed.</p>"

# Example usage (for local testing if needed):
# if __name__ == '__main__':
#     # This is a dummy data structure, similar to what resume_parser.py might produce.
#     sample_data = {
#         "name": "Alice Wonderland",
#         "title": "Chief Storyteller",
#         "email": "alice@wonderland.com",
#         "phone": "+123-456-7890",
#         "linkedin": "linkedin.com/in/alicew",
#         "github": "github.com/alicew",
#         "website": "alicewonderland.dev",
#         "summary": "Experienced in navigating rabbit holes and attending mad tea parties.\nSeeking new adventures in narrative construction.",
#         "experience": [
#             {
#                 "title": "Senior Croquet Player",
#                 "company": "Queen of Hearts Court",
#                 "dates": "Long Ago - Once Upon a Time",
#                 "description": "Played croquet with flamingos and hedgehogs.\nSpecialized in unfair advantages."
#             }
#         ],
#         "education": [
#             {
#                 "degree": "PhD in Nonsense",
#                 "institution": "Mad Hatter University",
#                 "dates": "A Few Years Back",
#                 "details": "Thesis on 'The philosophical implications of unbirthdays'.\nFurther notes here."
#             }
#         ],
#         "skills": ["Riddles", "Logic Puzzles (mostly illogical)", "Grinning Disappearing Acts"],
#         "projects": [
#             {
#                 "name": "Cheshire Cat Locator",
#                 "description": "A device to find that elusive cat.\nIt uses quantum entanglement.",
#                 "technologies": ["Quantum Entanglement", "Whimsy"],
#                 "link": "#"
#             }
#         ],
#         "profile_image_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=388&q=80"
#     }
#     # Ensure the template exists in ../templates/generated_portfolio_template.html relative to this file for this test to work.
#     # html_output = generate_portfolio_html(sample_data)
#     # print(html_output)
