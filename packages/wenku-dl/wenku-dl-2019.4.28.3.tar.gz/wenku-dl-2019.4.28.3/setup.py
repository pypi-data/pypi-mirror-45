from setuptools import setup, find_packages
import wenku_dl.__init__ as init
setup(
    name = 'wenku-dl',
    version=init.WENKU_DL_VERSION,
    license = "MIT Licence",
    description = "百度文库下载",

    author = 'YaronH',
    author_email = "yaronhuang@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires=["aigpy>=2019.4.28.1", "requests"],

    entry_points={'console_scripts': [
        'wenku-dl = wenku_dl:main', ]}
)
