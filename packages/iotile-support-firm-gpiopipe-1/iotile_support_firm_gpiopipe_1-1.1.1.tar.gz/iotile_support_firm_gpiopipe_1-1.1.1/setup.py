from setuptools import setup, find_packages

setup(
    name="iotile_support_firm_gpiopipe_1",
    packages=find_packages(include=["iotile_support_firm_gpiopipe_1.*", "iotile_support_firm_gpiopipe_1"]),
    version="1.1.1",
    install_requires=[],
    entry_points={'iotile.proxy': ['gpiopipe_proxy = iotile_support_firm_gpiopipe_1.gpiopipe_proxy']},
    author="Arch",
    author_email="info@arch-iot.com"
)