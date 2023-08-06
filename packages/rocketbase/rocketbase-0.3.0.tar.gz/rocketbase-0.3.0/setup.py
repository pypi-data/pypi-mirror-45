import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rocketbase',
    packages=setuptools.find_packages(),
    version='0.3.0',
    license='Proprietary',
    description='Making Machine Learning Available to everyone',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Mirage Technologies AG',
    author_email='hello@mirage.id',
    url='https://rocketbase.ai',
    keywords=['Automating', 'ML', 'Deployment', "PyTorch"],
    install_requires=[
        'tqdm',
        'requests',
        'google-cloud-storage'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
