import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="puissance4C",
    version="0.0.1",
    author="Robert Sebille",
    author_email="robert@sebille.name",
    maintainer = 'Robert Sebille',
    maintainer_email = 'robert@sebille.name',
    description="Puissance4C est un module puissance 4 en console et en\
     couleur, à jouer à 2.",
    license="GNU GPL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.adullact.net/zenjo/puissance4c/wikis/home",
    download_url = 'https://gitlab.adullact.net/zenjo/puissance4c/tree/master',
    #packages=setuptools.find_packages(),
    py_modules = ['puissance4C'],
    #packages = ['film'],
    #package_data={'film': ['frame/*', 'frames/*'],},
    #data_files = [('frame',['frame/poursuiteic', 'frame/poursuiteci', 'frame/roflflyingmoto']),
    #              ('frames',['frames/bon00', 'frames/bon10', 'frames/bon20', 'frames/bon30'])],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    ],
)
