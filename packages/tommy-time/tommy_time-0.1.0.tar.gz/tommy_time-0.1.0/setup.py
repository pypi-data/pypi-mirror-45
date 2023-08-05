import setuptools

with open('README.md','r',encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tommy_time',
    version='0.1.0',
    author='tommytju',
    author_email='1831412@tongji.edu.cn',
    description=long_description,
    long_desvription_content_type='text/markdown',
    url='https://space.bilibili.com/1900783',
    packages=setuptools.find_packages(),
    classfiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
)
    
