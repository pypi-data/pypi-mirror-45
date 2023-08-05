# PGAnonymizer

PGAnonymizer is a tool for anonymizing database for testing purposes.

## Installation
PGAnonymizer required Python 3.5 and above to run. PGAnonymizer can be installed using pip.
```sh
$ pip install git+https://git.proteus-tech.com/Boon/pganonymizer.git
```

## Background
PGAnonymizer will hash columns in table depending on the rules inside CSJ file.
### CSJ file format:
```
"table", "column", "rule"
"table_to_be_hased", "columned_to_be_hased", "rule_for_hashing"
"table_to_be_hased", "columned_to_be_hased", "rule_for_hashing"
"table_to_be_hased", "columned_to_be_hased", "rule_for_hashing"
```
#### Example for rules for hashing
`Hash` is for text type field such as name or address. The return value will be atmost 16 bytes
Example input:
```
Customer1
```
Example output:
```
20b7d291d71b2b1f
```
`Date` is for date type field. The return value will keep the original year but hash the month and date field.
Example input:
```
2000-12-15
```
Example output:
```
2000-01-10
```
`Phone` is for phone number. The return value will be of same length as the original number.
Example input:
```
+66932019385
```
Example output:
```
+66254818000
```
## Instruction
To use PGAnonymizer, you can call:
```sh
$ pganonymizer --schema path_to_schema_file.csj
```
For more information on the usage, please use the following command:
```sh
$ pganonymizer --help
```