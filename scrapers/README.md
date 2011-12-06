# What is this space for?

This space is contains the scripts for generating structured representations of Schema.org terms.

In order to generate variants (that is RDF, JSON or CSV versions) of the Schema.org terms, run the following Python script in the `scrapers` directory:

    scrape_all.py

To just generate a single variant, you can also use these guys:

    scrape_rdf.py
    scrape_json.py
    scrape_csv.py

They all either write to STDOUT or to a filename taken as command line argument.

There is also a script that generates all formats, does a bit of sanity checking to see if it worked, and copies them to a target directory. 

    cd scrapers
    ./run.rb temp-directory target-directory

This requires the [any23](http://developers.any23.org/) command line tool on the path.


## License

This software is Public Domain.


## Whom can I ask if I dunno what or how to do it

Ask Richard Cyganiak via Twitter ([@cygri](http://twitter.com/cygri)) or email (richard@cyganiak.de).
