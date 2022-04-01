# ChipWhisperer Simple Serial Glitch Target

This is a collection of the files used for the [ChipWhisperer Glitch Tutorial](https://chipwhisperer.readthedocs.io/en/latest/tutorials/courses_fault101_soln_fault%201_1%20-openadc-cwlitearm.html).

## Usage

> Note: when using this repository remember to pull in the submodule with 
> `git submodule update --init`.

To compile the file it is important to run:

```bash
make
```

To run the clock glitch:

```bash
python3 clock_glitch.py
```

## License

Licensed under a __MIT__ license.
