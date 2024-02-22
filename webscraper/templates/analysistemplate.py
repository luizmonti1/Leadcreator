import json
import os

def create_analysis_template(template_path, structure):
    """Create a JSON file for the analysis document template."""
    with open(template_path, 'w', encoding='utf-8') as file:
        json.dump(structure, file, indent=4)
    print(f"Template created at {template_path}")

def main():
    template_path = 'C:\\Users\\luizm\\webscraper\\templates\\analysis_template.json'
    os.makedirs(os.path.dirname(template_path), exist_ok=True)

    # Use the provided template structure
    template_structure = {
        "url": "",
        "segment": "",
        "seo_status": {
            "basic_seo_score": "",
            "on_page_seo": {
                "total_images": "",
                "images_with_alt_tags": "",
                "url_structure": "",
                "schema_markup_present": False
            },
            "technical_seo": {
                "ssl_certificate": False,
                "mobile_friendliness": False,
                "word_count": ""
            },
            "advanced_seo_analysis": {}
        },
        "load_time": {
            "Performance Score": "",
            "First Contentful Paint": "",
            "Speed Index": ""
        },
        "design_status": {
            "CSS Framework": "",
            "Mobile Usability": {},
            "Responsive Design": False
        },
        "pwa_features_status": {
            "score": "",
            "details": {}
        }
        # ... Add any other sections you need
    }

    create_analysis_template(template_path, template_structure)

if __name__ == "__main__":
    main()
