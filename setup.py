from setuptools import setup, find_packages

setup(
    name="port_intent_detector_pro",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "psutil>=5.9",
        "Flask>=2.3",
        "flask-socketio>=6.3",
        "PyQt6>=6.6",
        "plotly>=5.15",
        "reportlab>=3.8"
    ],
    entry_points={
        "console_scripts": [
            "port-intent-pro=cli:main",
            "port-intent-web-pro=webapp.app:run_web",
            "port-intent-desktop-pro=desktop.main:run_desktop"
        ]
    },
    python_requires='>=3.8',
)
