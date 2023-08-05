import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mly",
    version="0.0.11",
    author="Vasileios Skliris",
    author_email='vas.skliris@gmail.com',
    description='Dataset generation and tools for ML in gravitational waves',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://pypi.python.org/pypi/mly/',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "gwpy >= 0.13.1",
        "Keras >= 2.2.4",
        "tensorflow >= 1.12.0",
        "numpy >= 1.16.1",
        "sklearn"
    ]
)








data_generator_cbc(parameters=['cbc_01','real',25]       
                       ,length=4           
                       ,fs = 2048              
                       ,size =10            
                       ,detectors='HLV'  
                       ,spec=False
                       ,phase=False
                       ,res=128
                       ,noise_file=['20170825','SEG0_1187654416_2306s.txt']  
                       ,t=32             
                       ,lags=11
                       ,starting_point=200
                       ,name=''          
                       ,destination_path = null_path+'/datasets/cbc/'
                       ,demo=False)