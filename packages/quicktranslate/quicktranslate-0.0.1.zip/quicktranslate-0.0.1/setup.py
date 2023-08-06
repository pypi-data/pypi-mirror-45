from setuptools import setup,find_packages
setup(
    name="quicktranslate",
    version="0.0.1",
    description="translate with youdao,baidu and google",
    long_description="""
    you can use this in the command line,this is a example::

        trans -t example

    or::
        
        trans --trans example
    
    'example' means what you want to translate
    """,
    author='code-nick-python',
    author_email='2330458484@qq.com',
    license='MIT License',
    packages=find_packages(),
    url='https://github.com/code-nick-python/daily-tools/tree/master/translate_app',
    install_requires=[
        'requests',
        'bs4',
        'pyexecjs'
    ],
    entry_points = {
        'console_scripts': [
            'trans = translate_app:translate_main',
        ],
    }
)
