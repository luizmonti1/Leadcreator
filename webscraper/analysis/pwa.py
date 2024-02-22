import json
import requests
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import setup_logger, GOOGLE_API_KEY

# Configure logger for PWA analysis
pwa_logger = setup_logger('pwa_logger', 'pwa_analysis.log')

def analyze_service_worker_and_manifest(url):
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=pwa&key={GOOGLE_API_KEY}"
    try:
        response = requests.get(api_url)
        result = response.json()
        service_worker = result['lighthouseResult']['audits']['service-worker']['score'] == 1
        offline_access = result['lighthouseResult']['audits']['offline-start-url']['score'] == 1
        manifest_exists = result['lighthouseResult']['audits']['installable-manifest']['score'] == 1
        return {
            "Service Worker": "Present" if service_worker else "Absent",
            "Offline Access": "Supported" if offline_access else "Not Supported",
            "Web App Manifest": "Present" if manifest_exists else "Absent"
        }
    except Exception as e:
        pwa_logger.error(f"Error analyzing service worker and manifest for {url}: {e}")
        return {}


def analyze_pwa_features(url):
    pwa_logger.info(f"Starting PWA features analysis for {url}")

    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=pwa&key={GOOGLE_API_KEY}"

    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            pwa_logger.error(f"Error accessing PageSpeed Insights API: Status code {response.status_code}")
            return f"Error accessing PageSpeed Insights API: Status code {response.status_code}"

        result = response.json()

        # Extract PWA score and details
        pwa_score = result.get('lighthouseResult', {}).get('categories', {}).get('pwa', {}).get('score')
        pwa_audit_refs = result.get('lighthouseResult', {}).get('categories', {}).get('pwa', {}).get('auditRefs', [])

        pwa_details = {}
        for audit_ref in pwa_audit_refs:
            audit_id = audit_ref.get('id')
            audit_result = result.get('lighthouseResult', {}).get('audits', {}).get(audit_id, {})
            pwa_details[audit_id] = {
                'title': audit_result.get('title'),
                'description': audit_result.get('description'),
                'score': audit_result.get('score'),
                'details': audit_result.get('details')
            }

        # Additional logic to interpret scores and suggest improvements
        improvements = []
        for audit_id, audit_info in pwa_details.items():
            if audit_info['score'] is not None and audit_info['score'] < 1:
                improvements.append({
                    'area': audit_info['title'],
                    'advice': audit_info['description'],
                    'details': audit_info.get('details')
                })

        return {
            'score': pwa_score,
            'details': pwa_details,
            'improvements': improvements
        }
    except Exception as e:
        pwa_logger.error(f"Error in PWA Features Analysis for {url}: {e}")
        return f"Error in PWA Features Analysis: {e}"

# Example usage
if __name__ == "__main__":
    urls_to_analyze = [
        'https://www.davilledistribuidora.com.br/',
        'https://megag.com.br/',
        'https://www.prettidistribuidora.com.br/',
        'https://www.waze.com/',
        'https://www.quemfornece.com/',
        'https://produtosbrasileiros.co.uk/',
        'https://paiolatacado.com.br/',
        'https://www.visitcalifornia.com/',
        'https://tanakadistribuidora.com.br/',
        'https://www.volcafoods.com.br/',
        'https://www.themerchantboston.com/'
    ]

    for url in urls_to_analyze:
        result = analyze_pwa_features(url)
        pwa_logger.info(f"PWA Features Analysis for {url}: {result}")
