import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aaaahorodatage",
    version="0.0.1",
    author="Robert Sebille",
    author_email="robert@sebille.name",
    maintainer = 'Robert Sebille',
    maintainer_email = 'robert@sebille.name',
    description="Module python 3 de gestion d'horodatages. Chaque horodatage \
embarque son époque de référence et son fuseau horaire. L'époque de \
référence est configurable et peut être différente de l'époque Unix \
(1970-01-01T00:00:00) .",
    license="GNU GPL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://framagit.org/zenjo/AaaaHorodatage",
    download_url = 'https://framagit.org/zenjo/AaaaHorodatage/tree/master',
    #packages=setuptools.find_packages(),
    #py_modules = ['film', 'demo'],
    packages = ['aaaa'],
    package_data={
        'aaaa': ['./42'],
    },
    #data_files = [('frame',['frame/poursuiteic', 'frame/poursuiteci', 'frame/roflflyingmoto']),
    #              ('frames',['frames/bon00', 'frames/bon10', 'frames/bon20', 'frames/bon30'])],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    ],
)
