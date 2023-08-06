import setuptools

setuptools.setup(
     name='py-seleniumdrivers-chromedrivers',
     version='1.0.2',
     scripts=['download_drivers.sh'] ,
     author="Alexander Collins",
     author_email="alex@freighty.net",
     description="AWS Lambda Chromedrivers",
     long_description="",
     long_description_content_type="text/markdown",
     url="https://github.com/AlexanderCollins/py-seleniumdrivers-chromedrivers",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     include_package_data=True
 )
