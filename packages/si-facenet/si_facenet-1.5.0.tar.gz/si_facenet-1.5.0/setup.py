import setuptools


setuptools.setup(
    name="si_facenet",
    version="1.5.0",
    maintainer='Danny Delic',
    maintainer_email='delic.danny@gmail.com',
    include_package_data=True,
    description="A FaceNet-implementation for SI",
    long_description="SI interface for face recognition with Google's FaceNet deep neural network & TensorFlow",
    long_description_content_type="text/markdown",
    url="https://github.com/DanDyDunder/facenet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],install_requires=[
        'tensorflow==1.7', 'scipy', 'scikit-learn', 'opencv-python',
        'h5py', 'matplotlib', 'Pillow', 'requests'
    ]
)
