# Getting Our Characters in a Row

## Recap

Up to this point, we've processed each page of the Liber Primus, and extracted the characters (with very few exceptions). The extracted characters are currently represented as centroid-character pairs, where the centroid gives the location on the page of its corresponding character.

## Initial Attempts

Alright, so we have a list of true positive centroid-character pairs, but we're still an unorganized mess! Having the characters doesn't do us much good if we can't get the words. We need a way to organize the characters according to line, and then by their position in the line. The naive method would be to sort the centroids by y coordinate, and then by x coordinate. As shown below, this method won't work due to minute variance in the character centroids. 

|  Y  |  X  | Character |
|:---:|:---:|:---------:|
 729|  656| AE 
 729|  783| H 
 :|  :| :
 729| 1592| Y
 730|  617| R 
 :| :| :
 730| 1782| 1_dot
 731| 1014| F
 731| 1186| D

We need to find a more robust way of separating characters into their lines, from which point sorting by x coordinate should result in a correct transcription.

### Hard(ish) Coding

The first method I tried was hardly more complex than sorting. I examined exclusively the first image, taking the difference between the lowest and highest centroid on the page. Dividing the difference by 12 gave me an approximation of the step size between each line. I proceded to create evenly-spaced bins for each page using this step size as a fixed parameter. After each pair was binned, I rewrote the y coordinate to that of the bin, guaranteeing that all points in a given bin were perfectly aligned. From this point, sorting the pairs by y and then by x would produce a transcript. This method seemed reasonable, and certainly was functional as a first pass, but closer inspection of the pages shows that the line spacing is not always consistent. These slight changes could cause errors in my transcriptions that would be incredibly difficult to discover.

 Page 0 | Page 57
:------:|:-------:
![page 0](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/0_original.png "Page 0") | ![page 57](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/57_original.png "Page 57")

## Clustering Algorithms

If my hardcoding wasn't reliable, then I would be better off using a more flexible method. It was time for [clustering algorithms](https://en.wikipedia.org/wiki/Cluster_analysis)! I started off with the algorithm I was most familiar with: k-means.

### The k-means Debacle

[k-means](https://en.wikipedia.org/wiki/K-means_clustering) is an extremely simple and effective way of separating data into *k* clusters. k-means would be fantastic if we had a fixed number of lines in all the images, which we don't. So not only do we need a way to separate y coordinates into lines, but we also need to identify the number of lines in the image. Luckily, we just happen to have an algorithm for this task. Introducing...

#### Silhouette

[Silhouette](https://en.wikipedia.org/wiki/Silhouette_(clustering)) is a score that can be maximized to tentatively identify the correct number of clusters for a set of points. It essentially increases as clusters become denser, but also takes into account how close the clusters are to each other. Silhouette gives lower scores for too few clusters, because the clusters will naturally be less dense; silhouette also gives lower scores for too many clusters, because some of the clusters will be directly adjacent to each other.

#### Implementation

Implementing k-means and silhouette was a simple task, but the results I found were inconsistent. The *k* for which my silhouette score was maximized would change each iteration. After quadruple checking my code, I started graphing centroids to see what was going wrong...

 Whole Page Y Coordinates | Line 12 Y Coordinates
:------:|:-------:
![k-means](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/k_means.png "k-means") | ![k-means zoom](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/k_means_zoom.png "k-means Zoom")

In the images above, the character centroids are represented by circles and cluster centroids by triangles. On the left you can see several cluster centroids firmly fixed between two lines. At the same time, we see on the right that the 12th line has been split into two clusters. These plots were made after the algorithm reached a steady state, so why did this happen?

Upon further consideration, these results are perfectly natural. There is no mathematical factor repelling the centroids from each other, so two centroids can occupy a single line quite happily. Simultaneously, if one centroid moves between two lines, then there is no reason for centroids in adjacent lines to force the middle centroid to pick a line. The middle centroid is already twice as close to either line as their nearest neighbor would be. k-means simply won't work. We need an algorithm that will leverage the clear separation between the lines. After searching clustering algorithms, I found...

### DBSCAN

[DBSCAN](https://en.wikipedia.org/wiki/DBSCAN), or density-based spatial clustering of applications with noise, went above and beyond my needs. Not only is it connectivity-based, but it even removes noise (handy for any stray characters that might arise from the border art). After an easy implementation, we get the following results!

![dbscan](https://raw.githubusercontent.com/ralphatobe/cicada-3301/master/docs/img/dbscan.png "DBSCAN")

Perfect line segmentation! After sorting the clustered characters we finally have full transcripts ready for decryption!!

[return home](index.md)
