from distutils.core import setup

setup(
    name="fastparse",  # How you named your package folder (MyLib)
    packages=["fastparse"],  # Chose the same as "name"
    version="1",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="A fast way to get terminal arguments",  # Give a short description about your library
    author="ES3",  # Type in your name
    author_email="ourteamscare@gmail.com",  # Type in your E-Mail
    url="https://github.com/user/reponame",  # Provide either the link to your github or to your website
    download_url="https://github.com/elyassaf/Fast-Parse/archive/1.tar.gz",  # I explain this later on
    keywords=[
        "argparse",
        "cmd",
        "commandline",
        "command line",
        "terminal",
        "parsing",
        "parser",
        "args",
        "arguments",
    ],  # Keywords that define your package best
    install_requires=[],  # I get to this in a second
    classifiers=[
        "Development Status :: 5 - Production/Stable",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
