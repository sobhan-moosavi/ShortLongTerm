# Short and Long-term Pattern Discovery Over Large-Scale Geo-Spatiotemporal Data
This repo contains all the codes and sample files for the "Short and Long-term Pattern Discovery Over Large-Scale Geo-Spatiotemporal Data" paper 


## Short-term Pattern Discovery


## Long-term Pattern Discovery


## Data Pre-processing Steps


## Requirements 
The only requirement is ```Python```, version 2.7 is recommended. 


## How to Run
* __Extracting Short-term Patterns__: there are multiple steps to extract short-term patterns as follows:
  * __Extracting Events/Entities__: The first step is to extract traffic and weather events/entities from raw traffic and weather files, and create a dataset such as [Large-Scale Traffic and Weather Events Dataset](https://smoosavi.org/datasets/lstw). In ```0-CreateMixtureEventFile.py```, you may see thresholds, settings, and details on how to extract each type of traffic or weather event/entity. 
  * __Removing Redundant Traffic Events__: For this step, run ```1-RemoveRedundantTrafficEvents.py``` to remove duplicated geo-spatiotemporal entities/events. 
  * __Finding Child-Parent Relations__: Prior to building relation trees, we need to find child-parent relationship between each two geo-spatiotemporal entities. Use ```2-FindChildsParents.py``` to perform this step. 
  * __Creating Sequences of Relations__: This step is also prior to building relation trees, which creates sequences of relations between geo-spatiotemporal entities using ```3-FindSequencesOfPatterns.py```. 
  * __Extracting Tree Structures from Sequences__: This step creates relation trees based on previously extracted sequences of relations using ```4-ExtractTreesFromSequences.py```. 
  * __Mining Frequent Tree Patterns__: Finally, this step extract frequent embedded un-ordered tree patterns from a forest of relation trees using ```5-FindFrequentTreePatterns_revised_City.py```, which is based on [SELUTH](http://www.cs.rpi.edu/~zaki/www-new/pmwiki.php/Software/Software#sleuth) algorithm proposed by [Zaki 2005](http://www.cs.rpi.edu/~zaki/PaperDir/FI05.pdf). 


* __Extracting Long-term Patterns__:


## Dataset
A large-scale dataset of traffic and weather event data is used as input. Check [here](https://smoosavi.org/datasets/lstw) for the latest version of such a dataset. The data comes in the form of a single CSV file. We use the same data as input to both short and long-term pattern discovery processes. 


## Sample Results


## Acknowledgments 
* Moosavi, Sobhan, Mohammad Hossein Samavatian, Arnab Nandi, Srinivasan Parthasarathy, and Rajiv Ramnath. ["Short and Long-term Pattern Discovery Over Large-Scale Geo-Spatiotemporal Data."](https://arxiv.org/abs/1902.06792) Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. ACM, 2019. 

