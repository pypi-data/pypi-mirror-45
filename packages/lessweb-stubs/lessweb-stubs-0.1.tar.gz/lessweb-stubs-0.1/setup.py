from setuptools import setup
import os


name = 'lessweb-stubs'


def find_stub_files():
    result = []
    for root, dirs, files in os.walk(name):
        for file in files:
            if file.endswith('.pyi'):
                if os.path.sep in root:
                    sub_root = root.split(os.path.sep, 1)[-1]
                    file = os.path.join(sub_root, file)
                result.append(file)
    return result


setup(
    name = name,
    version='0.1',
    description='lessweb stubs「嘞是web」',
    long_description='\nREADME: https://github.com/qorzj/lessweb\n\n'
                     'Cookbook: http://lessweb.org',
    url='https://github.com/qorzj/lessweb',
    author='qorzj',
    author_email='inull@qq.com',
    license='MIT License',
    classifiers=[],
    install_requires=[
       'mypy>=0.660',
       'typing-extensions>=3.6.5'
    ],
    keywords='lessweb web web.py stubs',
    py_modules=[],
    packages = ['lessweb-stubs'],
    package_data={'lessweb-stubs': find_stub_files()},  # cp -r lessweb-stubs ~/dev/venv37/lib/python3.7/site-packages/
)