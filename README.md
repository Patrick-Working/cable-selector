# Cable-Selector
A simple tool to help retro console folks find the right cable for their device. 
This is a proof of concept and very much a work in progress.

How it works:
The program loads data from data.csv.
The first row of information in data.csv defines the labels for the the 6 drop down menus.
The following rows of CSV data outline a "valid choice", that is, when all 6 of the data entries are selected, the 7th data entry in the row will be displayed in the text box below. 

The program will not allow mismatched configutations, allowing the user to 'design' valid choices with long form csv entries. 

Quotations are required around the message information for it to be displayed correctly in the text box. Pipes (the '|' symbol) can be used to create breaks in the message data for multiple entries. URL's starting with HTTP:// will be clickable and launch a browser. 
