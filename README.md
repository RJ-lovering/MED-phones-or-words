# MED-phones-or-words
Small script for quantifying the difference between words, either orthographically or phonologically (as per CMUdict)

You'll need CMUdict, available with NLTK or from https://github.com/cmusphinx/cmudict, if you want to run the phonological component. 
All weights currently assigned are as determined by me, a linguist but not a phonologist. The four coordinates are approximate measures of quality, voicing, placement, and articulation. They were inputted by hand, not trained. Substitution cost is based on the difference between these vectors. In order to allow for free variation, the difference between coordinates is only 0.75, so that close substitution is less expensive than than deletion or insertion of a sound altogether.

The letter-based substitution calculation is based on a three-dimensional vector for each letter: [+consonant, +stop, +voice]. It's not as precise as it could be, but it gives more granularity than the usual replace/delete/insert trinary distinction.
