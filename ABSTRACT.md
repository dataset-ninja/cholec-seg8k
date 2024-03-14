The authors create **CholecSeg8k: A Semantic Segmentation Dataset for Laparoscopic Cholecystectomy Based on Cholec80** by extracting 8,080 laparoscopic cholecystectomy image frames from 17 video clips in [Cholec80](http://camma.u-strasbg.fr/datasets) and annotated the images. Each of these images are annotated at pixel level for thirteen classes, which are commonly founded in laparoscopic cholecystectomy surgery.

## Motivation

Endoscopy serves as a vital procedure for detecting, diagnosing, and treating conditions in organs that are typically challenging to examine without resorting to surgery, such as the esophagus, stomach, and colon. In clinical settings, an endoscopist guides the endoscope using a handle while simultaneously observing the recorded output video on an external monitor. However, the success of endoscopic procedures heavily relies on the operator's level of training and expertise. Factors like unsteady hand control and organ movement can significantly impact the accuracy of image analysis and surgical interventions. To aid surgeons in conducting endoscopic surgeries, various computer-assisted systems have been developed. These systems offer guidance and relevant contextual information to surgeons during operations. Some employ magnetic or radio-based external sensors to estimate and track the endoscope's position within the patient's body. However, these methods are susceptible to errors, making it challenging to achieve sub-centimeter localization accuracy.

An alternative approach, Simultaneous Localization and Mapping (SLAM), offers promising solutions. SLAM utilizes an image-based method to localize the camera with pixel-level accuracy, requiring no external infrastructure. This technique creates a real-time 3D map by comparing sensed data with reference data, providing an estimate of the camera's position in 3D space. Fortunately, reference data can be pre-collected using advanced technologies like 256-beam LiDAR and GPS-RTK to create high-definition point cloud maps. During runtime, less complex LiDAR systems can collect point cloud data, enabling localization with an accuracy of up to 5 centimeters. Implementing SLAM for endoscope navigation necessitates accurate semantic segmentation of images. This step is crucial for ensuring precise localization and navigation during procedures.

Accurate SLAM relies heavily on utilizing appropriate reference data for comparison. While GPS is commonly used in outdoor environments to obtain large-scale location data and retrieve corresponding reference data indexed by GPS coordinates, this method is impractical for endoscopic procedures. To address this challenge, one potential approach involves identifying the organs depicted in the images and using this information to query for the relevant reference data. The initial step can be accomplished through either semantic segmentation, which assigns object classes to each pixel, or object detection, which identifies object classes within bounding boxes. However, both semantic segmentation and object detection require well-labeled image datasets to train prediction networks, a resource that is not readily available for endoscope images.

## Dataset description

The authors construct an open semantic segmentation endoscopic dataset, which is available to medical and computer vision communities. This dataset consists of in total 8,080 frames extracted from 17 video clips in [Cholec80](http://camma.u-strasbg.fr/datasets) dataset. The annotation has thirteen classes.

<img src="https://github.com/dataset-ninja/cholec-seg8k/assets/120389559/6569f781-7b9a-48ef-aa33-d570f29ea83b" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Example of Semantic Segmentation Label of Endoscope Image.</span>

The CholecSeg8K dataset builds upon the endoscopic images sourced from Cholec80, a dataset originally published by the CAMMA (Computational Analysis and Modeling of Medical Activities) research group. This collaborative effort involved the University Hospital of Strasbourg, IHU Strasbourg, and IRCAD. The Cholec80 dataset comprises 80 videos capturing cholecystectomy surgeries conducted by 13 surgeons. Each video in Cholec80 was recorded at a frame rate of 25 frames per second and includes annotations detailing instruments and operation phases. In their work, the authors of CholecSeg8K selected a subset of closely related videos from the Cholec80 dataset. They then meticulously annotated semantic segmentation masks on frames extracted from these chosen videos. 

Data in CholecSeg8K Dataset are grouped into a two level directory for better organization and accessibility. Each directory on the first level collected the data of the ***video id*** clips extract from Cholec80 and is named by the filename of the video clips. Each directory on the secondary level tree stores the data for 80 images from the video clip and is named by the video filename and the frame index of the first image in the selected video clip. Each secondary level directory stores the raw image data, annotation, and color masks for 80 frames. There are a total of 101 directories and the total number of frames is 8,080. The resolution of each image is 854 pixels × 480 pixels.

During the pixel annotation process, the annotation classes were meticulously crafted to focus specifically on cholecystectomy surgeries, the primary operations targeted within the Cholec80 dataset. In particular, these annotation classes were designed to identify key anatomical structures such as the *liver* and *gallbladder*. To ensure comprehensive coverage, additional annotation classes were defined to encompass elements beyond the immediate scope of the surgeries. Notably, two classes were established with broader coverage. The first encompasses the gastrointestinal tract, encompassing structures like the stomach, small intestine, and adjacent tissues. The second class pertains to *liver* ligaments, including the coronary ligament, triangular ligament, falciform ligament, ligamentum teres (hepatis), ligamentum venosum, and lesser omentum. In this dataset, not all 13 classes appear in every frame at the same time.

| Class ID | Class Name            |
|----------|-----------------------|
| Class 0  | Black Background      |
| Class 1  | Abdominal Wall        |
| Class 2  | Liver                 |
| Class 3  | Gastrointestinal Tract|
| Class 4  | Fat                   |
| Class 5  | Grasper               |
| Class 6  | Connective Tissue     |
| Class 7  | Blood                 |
| Class 8  | Cystic Duct           |
| Class 9  | L-hook Electrocautery|
| Class 10 | Gallbladder           |
| Class 11 | Hepatic Vein          |
| Class 12 | Liver Ligament        |

<span style="font-size: smaller; font-style: italic;">Class numbers and their corresponding class names.</span>

The classes are not well balanced, which may lead to poor training results if using without cautions.

 Group with larger proportion             |  Group with smaller proportion
:-------------------------:|:-------------------------:
![](https://github.com/dataset-ninja/cholec-seg8k/assets/120389559/60fb8337-2093-43ea-b8c3-6fb55c2dbd63)  |  ![](https://github.com/dataset-ninja/cholec-seg8k/assets/120389559/ace71d73-392b-4011-830e-0c3bc638f02c)


<img src="https://github.com/dataset-ninja/cholec-seg8k/assets/120389559/baa85584-9b8a-4679-9827-5d4f74ab05a1" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Example of Semantic Segmentation Annotation of Gallbladder Endoscope Image.</span>

