from setuptools import setup

setup(
    name="bcca",
    version="1.7.0",
    description="Helpers from Base Camp Coding Academy",
    packages=["bcca"],
    install_requires=["pytest", "click", "colorama"],
    entry_points={
        "pytest11": ["bcca = bcca.pytest_plugin"],
        "console_scripts": [
            "what_have_i_done = bcca.what_have_i_done:main",
            "check_expect = bcca.test:main",
        ],
    },
)
