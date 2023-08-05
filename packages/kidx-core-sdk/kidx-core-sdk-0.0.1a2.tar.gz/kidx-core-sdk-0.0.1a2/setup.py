from setuptools import setup, find_packages
import io
import os

here = os.path.abspath(os.path.dirname(__file__))

# Avoids IDE errors, but actual version is read from version.py
__version__ = None
exec(open("kidx_core_sdk/version.py").read())

# Get the long description from the README file
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

tests_requires = ["pytest~=3.0", "pytest-pep8~=1.0", "pytest-cov~=2.0"]


install_requires = [
    "future~=0.16",
    "typing~=3.0",
    "requests~=2.20",
    "ConfigArgParse~=0.13.0",
    "coloredlogs~=10.0",
    "flask~=1.0",
    "flask_cors~=3.0",
    "gevent~=1.2",
    "six~=1.11",
]

extras_requires = {"test": tests_requires}

setup(
    name="kidx-core-sdk",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        # supported python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(exclude=["tests", "tools"]),
    version=__version__,
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_require=extras_requires,
    include_package_data=True,
    description="Machine learning based dialogue engine "
    "for conversational software.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kidx AI Technologies Education",
    author_email="nlp@mykidx.com",
    maintainer="Kidx NLP",
    maintainer_email="nlp@mykidx.com",
    license="Apache 2.0",
    keywords="nlp machine-learning machine-learning-library bot bots "
    "botkit kidx conversational-agents conversational-ai chatbot"
    "chatbot-framework bot-framework",
    url="https://rasa.com",
    download_url="http://git.mykidx.com/nlp/kidx_core_sdk/-/archive"
                 "/{}/kidx_core_sdk-{}.tar.gz"
    "".format(__version__, __version__),
    project_urls={
        "Bug Reports": "http://git.mykidx.com/nlp/kidx-nlu/issues",
        "Documentation": "https://docs.rasa.com/core",
        "Source": "http://git.mykidx.com/nlp/kidx_core_sdk",
    },
)

print("\nWelcome to Kidx Core SDK!")
print("If any questions please visit documentation page "
      "https://docs.rasa.com/core")
print("or join community chat on https://gitter.im/RasaHQ/rasa_core")
