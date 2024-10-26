from setuptools import setup

setup(
    name="ft_i18n",
    version="0.1",
    install_requires=["ft_i18n @ file://./ft_requests-0.1-py3-none-any.whl"],
    include_package_data=True,
    package_data={
        "ft_i18n": ["locale/*.json"],
    },
)
