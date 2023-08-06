from distutils.core import setup

setup(
    name = "EP_BHC",
    package = ["EP_BHC"],
    version = "1.2",
    license = "MIT",
    description = "A Python package to generate Bayesian hierarchical clusters to a supplied data",
    authors = "Eric Su and Min Chul Kim",
    author_email = "minchel93@gmail.com",
    url = "https://github.com/Eric-Su-2718/STA663-Final-Project",
    download_url = 'https://github.com/Eric-Su-2718/STA663-Final-Project/archive/v_01.tar.gz',
    keywords = ["BHC", "merge_nodes", "likelihood"],
    install_requires = [
        "numpy", 
        "cython"
    ],
     classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ]
)

