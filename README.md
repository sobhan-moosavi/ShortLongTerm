# Short and Long-term Pattern Discovery Over Large-Scale Geo-Spatiotemporal Data
This repo contains all the codes and sample files for the "Short and Long-term Pattern Discovery Over Large-Scale Geo-Spatiotemporal Data" paper 

## Short-term Pattern Discovery
Short-term or propagation patterns are those which show the impact of geo-spatiotemporal entities/events on a sequential basis, where one entity can be propagated and cause other entities to happen. One example is a _rain_ event which causes a _traffic accident_, and the _accident_ causes _traffic congestion_. 

## Long-term Pattern Discovery
Long-term or influential patters are those which show the impact of a temporally long geo-spatiotemporal entity on its spatial neighborhood. One example is a _major construction_ which causes more _traffic jams_ in its spatial neighborhood. 

## Requirements 
The only requirement is ```Python```, version 2.7 is recommended.

## Data Pre-processing Steps
Prior to performing any pattern extraction on traffic and weather data (as examples of geo-spatiotemporal data), there are two main pre-processing steps: 
  * __Extracting Events/Entities__: The first step is to extract traffic and weather events/entities from the raw traffic and weather data, and create a dataset such as [Large-Scale Traffic and Weather Events Dataset](https://smoosavi.org/datasets/lstw). In ```short-term/0-CreateMixtureEventFile.py```, you see a variety of processes, and empirically driven thresholds and settings to extract each type of traffic or weather event/entity. 
  * __Removing Redundant Traffic Events__: The second step is to remove duplicated geo-spatiotemporal entities/events using ```short-term/1-RemoveRedundantTrafficEvents.py```. 
 
## How to Run
* __Extracting Short-term Patterns__: there are multiple steps to extract short-term patterns as follows:
  * __Finding Child-Parent Relations__: Before building relation trees, we need to find the child-parent relationship between every two geo-spatiotemporal entities. Use ```short-term/2-FindChildsParents.py``` to perform this step. 
  * __Creating Sequences of Relations__: This step is also before building relation trees, which creates sequences of relations between geo-spatiotemporal entities using ```short-term/3-FindSequencesOfPatterns.py```. 
  * __Extracting Tree Structures from Sequences__: This step creates relation trees based on previously extracted sequences of relations using ```short-term/4-ExtractTreesFromSequences.py```. 
  * __Mining Frequent Tree Patterns__: Finally, this step extracts frequent embedded unordered tree patterns from a forest of relation trees using ```short-term/5-FindFrequentTreePatterns_revised_City.py```, which is based on [SELUTH](http://www.cs.rpi.edu/~zaki/www-new/pmwiki.php/Software/Software#sleuth) algorithm proposed by [Zaki 2005](http://www.cs.rpi.edu/~zaki/PaperDir/FI05.pdf). 


* __Extracting Long-term Patterns__:
  * __Preprocessing__: First we need to do some preprocessing over the data such as computing the duration of the events and modifying the type of the features accordingly. Use ```long-term/Process_steps/step1_preprocess.ipynb``` to perform this step.
  
<<<<<<< HEAD
  * __Extract long events__: The next step is finding the events which last longer than a threshold (300 minutes). After that, we merge the long events which happen to be in the same vicinity (radius of 14 miles). To do this step run ```long-term/Process_steps/step2_long_event_extraction.ipynb```.
=======
  * __Extract long events__: The next step is finding the events that last longer than a threshold (300 minutes). After that, we merge the long events that happen to be in the same vicinity (radius of 14 miles). Run ```long-term/Process_steps/step2_long_event_extraction.ipynb``` for this step. 
>>>>>>> a53a28721fe4e7cb704b3f87524b55ca3e0b6db3
  
  * __Sort long events__: We have to separate the long traffic events from long weather events since we have to process them differently. Simply run ```long-term/Process_steps/step3_sort_long_event.ipynb``` for this purpose. 
  
  * __Remove conflicts in long events__: There is a possibility that new merged events have conflicts with each other. We found them negligible so we just dropped them from the analysis. ```long-term/Process_steps/step4_check_and_remove_conflict.ipynb``` will perform this task. The merge of long-term events will occur in the second step (i.e. _Extract long events_). 
  
  * __Chunk data__: Since the data size is huge for parallel processing, we split data into multiple chunks. You can skip this step if your data size is not large or you do not want multiprocessing for any reason. The script is in ```long-term/Process_steps/step5_Chuck_events.ipynb```.
  
  * __Extract short events in proximity of long events__: The next step is finding all short events happened in the proximity of long events. Run python scripts in ```long-term/Process_steps/step6/```. Each script does the same job for each data chunk generated from previous steps. Note that generating proximity events for long traffic and weather events is different. The proximity of long traffic events is recognized by its distance to short events.  However, for the weather, it is based on its distance to the closest airport that reported the weather condition.
  
  * __Join the results__: ```long-term/Process_steps/step7_merge_dict_2_list.ipynb``` joins the results of the previous steps in case of using multiprocessing.
  
  * __Summerize the results__: Next we summarize the results and prepare them for the final statistical test. We extract the short events that happened during a long event in its vicinity and also short events before and after the long event. ```long-term/Final_Analysis_and_Plot/Final_analysis.ipynb``` summarizes and prepares the data.
  
  * __Run statistical test and plot results__: Finally apply the statistical test for analyzing the effect of long events on their neighborhood based on the type, time, and location. This is done by running ```long-term/Final_Analysis_and_Plot/Final_ploting_Original.ipynb```.




## Dataset
A large-scale dataset of traffic and weather event data is used as input. Check [here](https://smoosavi.org/datasets/lstw) for the latest version of such a dataset. The data comes in the form of a single CSV file. We use the same data as input to both short and long-term pattern discovery processes. 


<!-- ## Sample Results -->


## Acknowledgment
* Moosavi, Sobhan, Mohammad Hossein Samavatian, Arnab Nandi, Srinivasan Parthasarathy, and Rajiv Ramnath. ["Short and Long-term Pattern Discovery Over Large-Scale Geo-Spatiotemporal Data."](https://arxiv.org/abs/1902.06792) Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. ACM, 2019. 

```
@article{moosavi2019short,
  title={Short and Long-term Pattern Discovery Over Large-Scale Geo-Spatiotemporal Data},
  author={Moosavi, Sobhan and Samavatian, Mohammad Hossein and Nandi, Arnab and Parthasarathy, Srinivasan and Ramnath, Rajiv},
  booktitle = {Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery \&\#38; Data Mining},
  year = {2019},
  isbn = {978-1-4503-6201-6},
  location = {Anchorage, AK, USA},
  pages = {2905--2913},
  doi = {10.1145/3292500.3330755},  
  publisher = {ACM},
  address = {New York, NY, USA}
}
```
