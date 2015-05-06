This project implements Latent Relational analysis of word pairs using the method described by Peter D. Turney in his paper "Similarity of Semantic Relations"[1](1.md).

The implementation is in python & uses wordnet and google as data sources to derive semantic & statistical data for the calculations. However the module is implemented in a such a way that you can change the data sources to different sources without changing any other parts of the module

Since we are using google as a data source this module redistributes the xgoogle package[2](2.md) written by Peteris Krumins (thankyou very much) with some slight modifications for it to work with the current google (no doubt in future it will need updating when google changes there search result format).

Also I've added a small script to download articles from the pubmed. Its not perfect but incase someone needs its there. It uses e-utils API.

1. Turney, P. D. (2006). Similarity of semantic relations. Computational Linguistics, 32, 379-416. http://www.mitpressjournals.org/doi/pdfplus/10.1162/coli.2006.32.3.379
2. http://www.catonmat.net/blog/python-library-for-google-search/
3. http://www.ncbi.nlm.nih.gov/pubmed/