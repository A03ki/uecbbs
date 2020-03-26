from setuptools import setup


setup(
    name="twissify",
    version="0.5.0",
    description="The package to classify the photo tweet",
    author="A03ki",
    install_requires=["numpy", "pillow", "tweepy"],
    url="",
    license="MIT License",
    packages=["twissify",
              "tests"],
    test_suite="tests"
)
