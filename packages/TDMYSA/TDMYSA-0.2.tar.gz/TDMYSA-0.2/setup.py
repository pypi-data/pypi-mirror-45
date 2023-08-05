from setuptools import setup

long_description=""" TDMYSA """
	
	
setup(name='TDMYSA',
      version='0.2',
      description='scores',
	  long_description=long_description,
	  url='https://shahabks.github.io/Speech-Rater/',
      author='Shahab Sabahi',
      author_email='shahab.sabahi@gmail.com',
      license='MIT',
      classifiers=[
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.7',
		],
	  keywords='acoustic and signal processing',
	  install_requires=[
		'numpy>=1.15.2',
		'praat-parselmouth>=0.3.2',
		'pandas>=0.23.4',
		'scipy>=1.1.0',
		'SpeechRecognition>=3.8.1',
		'langdetect>=1.0.7',
		'nltk>=3.4',
		'scikit-learn>=0.20.1',
		'textatistic>=0.0.1',
		'textblob>=0.15.3',
		],
	  packages=['TDMYSA'],
      zip_safe=False) 
