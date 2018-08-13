#Product Catalogue

This algorithm converts the data in the article-files into the specified de-normalized matrix representation and stores 
the results in an output file.

Takes as parameters:
(input) The file that stores information on all available parts.
(input) The file that stores the assignment of parts and colors to articles.
The parameters are passed to the Python script by name and not by position.It uses the argparse package to parse the parameters. 

Writes Out:
(output) The de-normalized matrix representation, written to a file.

Use Case: 
An article is identified by an article code (ARTICLE_CD) and consists of multiple parts, which have got a color. 
A part is identified by its part number (PART_NO). A list of all available parts an article can consist of is attached in a
pipe "|" delimited file ```mockup_data_parts.dsv```. The file format is PART_CD|PART_NO. 

The assignment of parts and colors to articles is stored in a pipe "|" delimited file ```mockup_data_articles.dsv```
and follows the format ARTICLE_CD|PART_NO|COLOR. Example: "06MAWOXF08|0|Purple" means that the article with the code 
"06MAWOXF08" consists of part "0" and the color of this part is "Purple".("").A specific article does not 
have to consist of all the available parts. For the sake of convenience, we need to convert the article file into a 
denormalized matrix representation, where every row describes one article.The first column indicates the article number, 
the consecutive columns all possible parts of an article. Both the article codes and the part numbers should occur in 
ascending order. In case an article does not consist of a specific part, the column should be empty. The file format for the
output file should be ARTICLE_CD|PART_0|PART_1|...|PART_X.
    
Example:   
ARTICLE_CD|PART_0|PART_1|...|PART_X
B12345|Black||...|Yellow

Article "B12345" consists of part "0", which is "Black", does not consist of part "1" and consists of part "X", which is "Yellow".
