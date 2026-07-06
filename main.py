"""
Radio AI PRO - Complete Standalone Entry Point for PyCharm
This file can be run directly from PyCharm without module path issues
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Now import the app
try:
    from ui.app import RadioAIPro
    
    if __name__ == "__main__":
        print(f"Starting Radio AI PRO from {project_root}")
        print(f"Python path: {sys.path[0]}")
        
        app = RadioAIPro()
        app.update_clock()
        app.mainloop()
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print(f"\nMake sure you have all required files in: {project_root}")
    print("\nRequired structure:")
    print("""
    C:\\RadioAIpro\\
    ├── __init__.py
    ├── main.py (this file)
    ├── requirements.txt
    ├── models/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── track.py
    │   ├── prompt.py
    │   ├── dagdeel.py
    │   └── event.py
    ├── api/
    │   ├── __init__.py
    │   ├── radioboss.py
    │   ├── openai_tts.py
    │   └── weather.py
    ├── services/
    │   ├── __init__.py
    │   ├── state_manager.py
    │   ├── prompt_engine.py
    │   ├── wiki_fetcher.py
    │   ├── scheduler.py
    │   ├── dagdeel_manager.py
    │   └── event_manager.py
    ├── ui/
    │   ├── __init__.py
    │   ├── app.py
    │   └── components/
    │       ├── __init__.py
    │       ├── common.py
    │       ├── dashboard.py
    │       ├── prompts.py
    │       ├── settings.py
    │       ├── dagdeel.py
    │       └── events.py
    ├── utils/
    │   ├── __init__.py
    │   ├── constants.py
    │   ├── logger.py
    │   └── validators.py
    └── tests/
        ├── __init__.py
        ├── test_dagdeel_manager.py
        └── test_event_manager.py
    """)
    sys.exit(1)

except Exception as e:
    print(f"❌ Application Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
