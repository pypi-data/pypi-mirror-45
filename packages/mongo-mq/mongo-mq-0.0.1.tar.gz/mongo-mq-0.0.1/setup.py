from setuptools import setup, find_packages

setup(name='mongo-mq',
      version="0.0.1",
      author='Zaytsev Dmithry',
      author_email='zaytsev_dmitriy@aol.com',
      description="A queue using mongo as backend storage.",
      long_description=open("README.rst").read(),
      url='https://github.com/dzaytsev91/mongomq',
      license='BSD-derived',
      packages=find_packages(),
      install_requires=["pymongo", "mongonose"],
      setup_requires=["nose", "mongonose"],
      include_package_data=True,
      zip_safe=True,
)
