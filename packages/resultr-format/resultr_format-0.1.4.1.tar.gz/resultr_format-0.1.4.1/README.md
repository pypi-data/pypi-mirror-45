#  resultr-format
>  back end for [resultr](https://github.com/haykkh/resultr)   

resultr-format lets [resultr](https://github.com/haykkh/resultr):
  * get your weighted average for a year
  * get your rank in your year
  * re-format the results by module (as below) and output to csv

output format:

**Devcom**|**PHAS0000**|**PHAS0001**|**PHAS0002**|**PHAS0003**|**PHAS0004**|**PHAS0005**|**PHAS0006**|**PHAS0007**|**Averages**
:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:
100|99|98|97|96|95|94|93|92|95.5
24|3|55|34|93|43|15|25|40|39 

## Release History

* 0.1.4.1
    * Forgot to initialise goodFormater when i fixed devcom bug
* 0.1.4
    * Fixed devcom bug for year 3+ people
* 0.1.3.1
    * convert 'DA' results to 0 in badFormater
* 0.1.3
    * Convert 'DA' results to 0
* 0.1.2.3
    * Added .upper() to key in badformater incase 'cand'/'Cand'/'CAND'
* 0.1.2.2
    * Changed form doing .upper() in badformater to doing it in goodformater
* 0.1.2.1
    * Changed from doing .upper() to each row in badformater to key.upper():val.upper()
* 0.1.2
    * Changed badformater to import everything uppercase
* 0.1.1
    * goodFormatter would throw key error when popping '0' if '0' didn't exist
* 0.1.0
    * The first proper release


## Meta

Hayk Khachatryan – hi@hayk.io

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/haykkh](https://github.com/haykkh/)

## Contributing

1. Fork it (<https://github.com/haykkh/resultr-format/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
