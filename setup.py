from setuptools import setup

LONG_DESC = open("README.md").read()

setup(
    name="wall-resize",
    version="1.0.0b1",
    description="Resizes wallpapers to desired size",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
    ],
    url="https://github.com/slapelachie/wall-resize",
    author="slapelachie",
    author_email="lslape@slapelachie.xyz",
    license="GPLv2",
    packages=["wall_resize", "wall_resize.utils"],
    entry_points={"console_scripts": ["wall-resize=wall_resize.__main__:main"]},
    install_requires=["tqdm", "Pillow"],
    zip_safe=False,
)