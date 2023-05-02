from __future__ import annotations
from setuptools import find_packages, setup
from face_morphing_tool.setup.version import get_version

def install_requirements(filename="requirements.txt"):
    try:
        from pip.req import parse_requirements
    except ImportError:
        from pip._internal.req import parse_requirements
    
    try:
        from pip.download import PipSession
    except ImportError:
        from pip._internal.network.session import PipSession
    
    links = []
    requires = []

    try: 
        requirements = parse_requirements(filename)
    except:

        requirements = parse_requirements(filename, session=PipSession())
    
    for item in requirements:
        if getattr(item, "url", None):
            links.append(str(item.url))
        
        if getattr(item, "link", None):
            links.append(str(item.link))
        
        req = item.req if hasattr(item, "req") else item.requirement

        if req:
            requires.append(str(req))
    
    return requires, links


with open("README.md") as f:
    readme = f.read()



setup(
    name="face-morphing-tool",
    packages=find_packages(),
    author="Jake Kugel, Shu Xu, Richwell Perez",
    description="Final project for UIUC CS445 - Computational photograhy",
    long_description=readme,
    license="MIT",
    url="https://github.com/jakekugel/Face-Morphing.git",
    version=str(get_version),
    python_requires=">=3.8",
    install_requires=install_requirements(),
    entry_points={
        "console_scripts":[
            "face-morphing=face_morphing_tool.app.do_morphing:main",
        ],
    }
)