# log_parser
papertrail log parser in python


- main code -> main.py
- main input file -> dummy.json
- main output file -> output.csv

### Note - Output file can be generated by redirecting the output of main.py


for running query on the csv.

1) Navigate to the binary inside q-2.0.9/bin/q folder
2) sample query ./q-2.0.9/bin/q "SELECT c7,count(c7) FROM output.csv GROUP BY c7" 
3) ./q-2.0.9/bin/q "SELECT c2,count(c2) FROM output.csv GROUP BY c2"  
