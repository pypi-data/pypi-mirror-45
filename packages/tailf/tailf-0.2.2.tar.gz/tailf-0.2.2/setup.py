from setuptools import setup

setup(
    name="tailf",
    version="0.2.2",
    description="tail -f functionality for your python code",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # "Operating System :: POSIX :: Linux",  # some features are linux-only
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="http://gitlab.com/trooniee/tailf",
    author="Sergei Shilovsky",
    author_email="sshilovsky@gmail.com",
    license="MIT",
    packages=["tailf"],
    # install_requires=['inotify;platform_system=="Linux"'],
    zip_safe=False,
    test_suite="nose.collector",
    tests_require=["nose"],
)
