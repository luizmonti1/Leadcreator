import json
import logging
import os

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_networking_data(entry):
    networking_data = {
        'url': entry.get('url'),
        'emails': entry.get('emails', []),
        'phone': entry.get('phone')
    }
    return networking_data


def extract_seo_data(entry):
    seo_data = {
        'total_images': entry['on_page_seo']['total_images'],
        'images_with_alt_tags': entry['on_page_seo']['images_with_alt_tags'],
        'url_structure': entry['on_page_seo']['url_structure'],
        'schema_markup_present': entry['on_page_seo']['schema_markup_present'],
        'ssl_certificate': entry['technical_seo']['ssl_certificate'],
        'mobile_friendliness': entry['technical_seo']['mobile_friendliness'],
        'word_count': entry['technical_seo']['word_count'],
        'basic_seo_score': entry['seo_status']['basic_seo_score'],
        'additional_seo_data': entry['seo_status']['additional_seo_data'],
        'advanced_seo_analysis': entry['seo_status']['advanced_seo_analysis'],
    }

    # Extracting basic SEO details
    basic_seo_details = entry['seo_status']['basic_seo_details']
    for detail in basic_seo_details:
        seo_data[f"basic_seo_detail_{detail['id']}"] = {
            'weight': detail['weight'],
            'group': detail.get('group', 'N/A')  # Use .get() to avoid KeyError if 'group' is not present
        }

    # Extracting keyword optimization details, if available
    keyword_counts = entry['seo_status'].get('advanced_seo_analysis', {}).get('keyword_optimization', {}).get('keyword_counts', {})
    for keyword, count in keyword_counts.items():
        seo_data[f"keyword_{keyword}"] = count

    return seo_data



def extract_load_time_data(entry):
    load_time_data = {
        'performance_score': entry.get('Performance Score', 0),
        'first_contentful_paint': entry.get('First Contentful Paint', 'N/A'),
        'speed_index': entry.get('Speed Index', 'N/A'),
        'time_to_interactive': entry.get('Time to Interactive', 'N/A'),
        'first_meaningful_paint': entry.get('First Meaningful Paint', 'N/A'),
        'total_blocking_time': entry.get('Total Blocking Time', 'N/A'),
        'largest_contentful_paint': entry.get('Largest Contentful Paint', 'N/A'),
        'cumulative_layout_shift': entry.get('Cumulative Layout Shift', 'N/A'),
        'critical_request_chains': entry.get('Critical Request Chains', 'N/A'),
        'javascript_execution_time': entry.get('JavaScript Execution Time', 'N/A'),
        'main_thread_work_breakdown': entry.get('Main Thread Work Breakdown', 'N/A'),
        'offscreen_images': entry.get('Offscreen Images', 'N/A'),
        'efficiently_encode_images': entry.get('Efficiently Encode Images', 'N/A'),
        'text_compression': entry.get('Text Compression', 'N/A'),
        'render_blocking_resources': entry.get('Render-Blocking Resources', 'N/A'),
        'server_response_time': entry.get('Server Response Time', 'N/A'),
        'uses_efficient_image_formats': entry.get('Uses Efficient Image Formats', 'N/A'),
        'minified_javascript': entry.get('Minified JavaScript', 'N/A'),
        'minified_css': entry.get('Minified CSS', 'N/A'),
        'properly_sized_images': entry.get('Properly Sized Images', 'N/A'),
        'third_party_payloads': entry.get('Third-Party Payloads', 'N/A'),
        'render_blocking_resources_count': entry.get('Render-Blocking Resources Count', 0)
    }

    # Extracting Opportunities for Optimization
    opportunities = entry.get('Opportunities for Optimization', {})
    for opp_key, opp_value in opportunities.items():
        load_time_data[f"optimization_{opp_key}"] = {
            'description': opp_value.get('Description', 'N/A'),
            'estimated_savings': opp_value.get('Estimated Savings', 'N/A')
        }

    return load_time_data


def extract_design_status_data(entry):
    design_status_data = {
        'css_framework': entry.get('CSS Framework', 'N/A'),
        'modern_javascript_usage': entry.get('Modern JavaScript Usage', 'N/A'),
        'responsive_design': entry.get('Responsive Design', 'N/A'),
        'html5_usage': entry.get('HTML5 Usage', 'N/A'),
        'accessibility_features': entry.get('Accessibility Features', 'N/A')
    }

    # Extracting Mobile Usability data
    mobile_usability = entry.get('Mobile Usability', {})
    for key, value in mobile_usability.items():
        design_status_data[f"mobile_usability_{key.replace(' ', '_').lower()}"] = value

    # Extracting PageSpeed Insights data
    page_speed_insights = entry.get('PageSpeed Insights', {})
    for key, value in page_speed_insights.items():
        design_status_data[f"page_speed_insights_{key.replace(' ', '_').lower()}"] = value

    return design_status_data


def extract_pwa_features_status_data(entry):
    pwa_features_data = {
        'pwa_score': entry.get('score', 0),
        'details': {}
    }

    # Process 'details' section
    details = entry.get('details', {})
    for feature, detail in details.items():
        if detail is not None:
            pwa_feature_detail = {
                'title': detail.get('title', 'N/A'),
                'description': detail.get('description', 'N/A'),
                'score': detail.get('score', 'N/A'),
                'reasons': [item.get('reason', 'N/A') for item in detail.get('details', {}).get('items', [])] if detail.get('details') else []
            }
            pwa_features_data['details'][feature] = pwa_feature_detail

    # Process 'improvements' section
    improvements = entry.get('improvements', [])
    pwa_features_data['improvements'] = []
    for improvement in improvements:
        if improvement is not None:
            imp_detail = {
                'area': improvement.get('area', 'N/A'),
                'advice': improvement.get('advice', 'N/A'),
                'reasons': [item.get('reason', 'N/A') for item in improvement.get('details', {}).get('items', [])] if improvement.get('details') else []
            }
            pwa_features_data['improvements'].append(imp_detail)

    return pwa_features_data



def save_data_to_file(data, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving data to {filename}: {e}")


def main():
    folder_path = 'C:\\Users\\luizm\\webscraper\\clientes\\www.estudiomalagueta.com.br'
    file_names = [
        'design_status.json',
        'load_time.json',
        'networking.json',
        'pwa_features_status.json',
        'seo_status.json'
    ]
    output_folder = 'C:\\Users\\luizm\\webscraper\\phase3\\parsed_data.json'

    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                entry = json.load(file)

            if file_name == 'seo_status.json':
                seo_status_data = extract_seo_data(entry)
                save_data_to_file(seo_status_data, os.path.join(output_folder, f'{file_name[:-5]}_data.json'))

        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {file_path}: {e}")


if __name__ == "__main__":
    main()
