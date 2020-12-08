 # Systematic approach for deep object detectionusing CAD models

## Master's dissertation work at the UFF Computing Institute

Object Detection (OD) is an important vision problem for industry, which can be used for quality control in the production lines. Recently, deep learning methods have enabled training OD models with very good performance for complex real world datasets. However, the adoption of these models in industry has been limited by the difficulty --- and the significant cost --- of collecting high quality training datasets. On the other hand, OD for quality control in production lines presents the specificity of often having CAD models available for the objects to be detected. In this paper, we introduce a fully automated method that uses a CAD model of an object and returns a fully trained OD model for detecting this object. To do this, we created a Blender script that generates realistic datasets of images containing the CAD model as well as the corresponding OD labels. These datasets are then used for training the object detectors. The method is validated experimentally on a practical example, and we show that this approach can generate OD models performing well on real images, while being trained only on synthetic images.

In the Python_Codes directory, it is possible to access the codes used in this project.

The lib directories contain the .stl and .obj files used to generate the synthetic images.

The dataset of images and labels separated by objects can be accessed through the link: link kaggle
