# UCI SMS Spam Collection data notice

## Primary dataset

The primary runtime dataset is the **SMS Spam Collection** from the UCI Machine Learning Repository. It contains 5,574 labeled SMS messages in one text file. Each line contains a class label, one tab character, and the raw message.

- Classes: `ham` and `spam`
- UCI dataset page: https://archive.ics.uci.edu/dataset/228/sms+spam+collection
- Official archive used by the program: https://archive.ics.uci.edu/static/public/228/sms%2Bspam%2Bcollection.zip
- DOI: https://doi.org/10.24432/C5CC84
- License listed by UCI: Creative Commons Attribution 4.0 International, CC BY 4.0

Formal citation supplied by UCI:

> Almeida, T., & Hidalgo, J. (2011). *SMS Spam Collection* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84

The script stores the complete downloaded text file as:

```text
data/SMSSpamCollection
```

The complete data file is validated before training. Primary mode requires exactly 5,574 nonblank records, only the labels `ham` and `spam`, one tab separator per record, and at least one record in each class.

## Bundled sample

`SMSSpamCollection.sample` contains the first 100 records from a public mirror of the same UCI text file. It is included only so the parser, classifier, equations, tests, and terminal output can run in an environment without external network access.

Observed sample properties:

```text
Records:       100
HAM records:    83
SPAM records:   17
Encoding:       UTF-8
SHA-256:        cbaf636cfa6f1c3beff9ec7d09acf5aaa733d04b918af5dd5afefa7ffbc13ce2
```

Transport mirror used to obtain the sample:

```text
https://github.com/justmarkham/DAT5/blob/master/data/SMSSpamCollection.txt
```

The mirror is not treated as the authoritative source. UCI remains the source for the dataset identity, record count, DOI, and license.

## Required use distinction

- Default mode uses or downloads the complete UCI dataset.
- `--sample-data` explicitly selects the 100-message sample.
- The program never silently substitutes the sample for the complete dataset.
- Probabilities produced in sample mode are teaching results fitted to 100 messages. They are not the complete-corpus model probabilities.
