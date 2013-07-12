cs373-wcdb
==========

*Identify common attributes of the data and insure that every data item has a value for that attribute. 
 
*Post the schema and instance to the public repository.

*Create an import/export facility from the XML into the Django models and back using ElementTree.

*It must be password protected.

*It must not crash when given a bad file.

*It must report an error if the XML being imported does not match the schema using MiniXsv.

*The export facility must export from the Django models to the screen in a way that is recognizable as XML.

*Hint: There is a way to set the HTTP Content-Type to be text/wcdb1.

*Create a static HTML page for three crises, three organizations, and three people that displays all of the data collected.

*The pages must be served by Django.

*Create a set of unittest tests.

*Write an initial technical report.




* Link to contact info Google Doc: https://docs.google.com/document/d/17aQGjf3V3MqLfxaajcE33ir3tT16l-LHZWrXc9HL-fU/edit?usp=sharing

* Link to Unique Crises, People, Places Google Doc: https://docs.google.com/spreadsheet/ccc?key=0AkNfAw_ZzZ1MdENHSGxXN005dmVDSDN1OXBBX3pNMkE#gid=0

* Link to shared schema for WorldCrisis.xml on Piazza: https://github.com/aaronj1335/cs373-wcdb1-schema

* Link to .xml https://docs.google.com/document/d/1kBrdjG4wTqb4msC9a6_fvnBs_p3F9Q9ZlLE-g-73HRY/edit?usp=sharing

* Link to public WCDB database: http://wcdb.quiri.co
  * username: gummy_pandas
  * password: saucysalamander

* MySQL Info
 
   user = hnp248
   database = cs373_hnp248
   password = TbWNGpEkMj
  
   user = lemus
   database = cs373_lemus
   password = 7leuEjJU2x

   /u/z/users/cs373/lemus

   mysql -h z -u lemus -p7leuEjJU2x
