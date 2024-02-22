import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import OPENAI_API_KEY, ORGANIZATION
from openai import OpenAI

client = OpenAI(
  organization=ORGANIZATION,
  api_key=OPENAI_API_KEY
)

def personalized_instructions(site_data):
    seo_analysis = json.loads(site_data.get('seo_status', '{}'))
    load_time_analysis = json.loads(site_data.get('load_time', '{}'))
    design_analysis = json.loads(site_data.get('design_status', '{}'))
    pwa_analysis = json.loads(site_data.get('pwa_features_status', '{}'))

    # Customize the email body here
    email_body = f"""
    Olá,

    Meu nome é Bruno Bianchini, e sou SEO/Analista de Dados na Agência Freela.

    Analisamos o site da {site_data['segment']} e aqui estão nossas descobertas e recomendações:

    {seo_analysis}
    {load_time_analysis}
    {design_analysis}
    {pwa_analysis}

    Para discutir essas oportunidades em detalhes, por favor entre em contato.

    Atenciosamente,
    Bruno Bianchini
    bruno@agenciafreela.com.br
    +55 11 99538-1987
    """

    return email_body.strip()

def generate_email(site_data, temperature=0.7):
    prompt = personalized_instructions(site_data)
    
    response = client.completions.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=temperature,
        max_tokens=1000  # Update the maximum token length here
    )
    return response.choices[0].text.strip()

def process_bulk_report(json_file, output_file):
    try:
        with open(json_file, 'r') as file, open(output_file, 'w') as output:
            data = json.load(file)
            for row in data[0]['rows']:
                site_data = {
                    'url': row[0],
                    'segment': row[1],
                    'seo_status': row[2],
                    'load_time': row[3],
                    'design_status': row[4],
                    'pwa_features_status': row[5]
                }
                email_content = generate_email(site_data)
                output.write(f"Email for {site_data['url']}:\n{email_content}\n\n")
                print(f"Processed {site_data['url']}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
process_bulk_report('C:\\Users\\luizm\\webscraper\\database_report.json', 'C:\\Users\\luizm\\webscraper\\email_output.txt')

