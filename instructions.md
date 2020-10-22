# Instructions

1. Download the raw data in PDF format from [NCSL](https://www.ncsl.org/research/about-state-legislatures/partisan-composition.aspx). (Note these are currently present in the "raw" directory.)
 - [2020](https://www.ncsl.org/Portals/1/Documents/Elections/Legis_Control_2020_April%201.pdf)
 - [2019](https://www.ncsl.org/Portals/1/Documents/Elections/Legis_Control_2019_February%201st.pdf)
 - [2018](https://www.ncsl.org/Portals/1/Documents/Elections/Legis_Control_011018_26973.pdf)
 - [2017](https://www.ncsl.org/Portals/1/Documents/Elections/Legis_Control_2017_March_1_9%20am.pdf)
 - [2016](https://www.ncsl.org/portals/1/documents/elections/Legis_Control_2016.pdf)
 - [2015](https://www.ncsl.org/Portals/1/Documents/Elections/Legis_Control_2015.pdf)
 - [2002-2014](https://www.ncsl.org/documents/statevote/legiscontrol_2002_2014.pdf)
 - [1990-2000](https://www.ncsl.org/documents/statevote/legiscontrol_1990_2000.pdf)
 - [1978-1988](https://www.ncsl.org/documents/statevote/legiscontrol_1978_1988.pdf)

2. Convert documents to xml with pdftohtml utility (currently in xml directory). Example for 2020:

 `pdftohtml -xml 'raw/Legis_Control_2020_April 1.pdf' -stdout > xml/2020.xml`
