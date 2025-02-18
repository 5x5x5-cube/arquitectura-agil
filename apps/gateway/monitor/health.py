import requests

def get_system_health():
    health_status = {}

    # List of services to check
    services = {
        'Service A': 'http://service-a/health',
        'Service B': 'http://service-b/health',
        'Service C': 'http://service-c/health',
    }

    for service_name, url in services.items():
        try:
            response = requests.get(url, timeout=2)
            health_status[service_name] = {
                'status': response.status_code,
                'message': response.json().get('message', 'No message provided')
            }
        except requests.exceptions.RequestException as e:
            health_status[service_name] = {
                'status': 'down',
                'message': str(e)
            }

    return health_status