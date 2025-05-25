import unittest
import sys
import os
import json
from typing import Dict, Any

# Voeg de hoofdmap toe aan het Python pad
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def configure_environment():
    """Configureer de omgevingsvariabelen voor de tests."""
    # Stel het standaard model in op openchat:latest
    os.environ['DEFAULT_LLM_MODEL'] = 'openchat:latest'
    
    # Optioneel: Voeg hier andere omgevingsvariabelen toe die nodig zijn voor de tests
    os.environ['TEST_ENV'] = 'true'

def run_tests() -> Dict[str, Any]:
    """Voer de tests uit en retourneer de resultaten."""
    # Configureer de omgeving
    configure_environment()
    
    print("\n\033[94m=== Configuratie ===\033[0m")
    print(f"Gebruikt model: \033[93m{os.environ.get('DEFAULT_LLM_MODEL', 'niet ingesteld')}\033[0m")
    print(f"Testomgeving: \033[93m{'actief' if os.environ.get('TEST_ENV') == 'true' else 'inactief'}\033[0m")
    print("\033[94m===================\033[0m\n")
    
    # Laad en voer de tests uit
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    
    # Voer de tests uit met gedetailleerde uitvoer
    test_runner = unittest.TextTestRunner(
        verbosity=2,  # Toon gedetailleerde uitvoer
        failfast=False,  # Ga door na een gefaalde test
        buffer=True  # Toon alleen output van geslaagde tests als ze falen
    )
    
    result = test_runner.run(test_suite)
    
    # Retourneer de testresultaten
    return {
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'skipped': len(result.skipped),
        'was_successful': result.wasSuccessful()
    }

if __name__ == '__main__':
    # Voer de tests uit en krijg de resultaten
    test_results = run_tests()
    
    # Toon een samenvatting van de testresultaten
    print("\n\033[94m=== Test Samenvatting ===\033[0m")
    print(f"Totaal aantal uitgevoerde tests: \033[93m{test_results['tests_run']}\033[0m")
    print(f"Aantal fouten: \033[91m{test_results['errors']}\033[0m")
    print(f"Aantal gefaalde tests: \033[91m{test_results['failures']}\033[0m")
    print(f"Aantal overgeslagen tests: \033[93m{test_results['skipped']}\033[0m")
    
    if test_results['was_successful']:
        print("\n\033[92m✓ Alle tests zijn succesvol doorlopen!\033[0m")
    else:
        print(f"\n\033[91m✗ Niet alle tests zijn geslaagd. Totaal fouten: {test_results['errors'] + test_results['failures']}\033[0m")
