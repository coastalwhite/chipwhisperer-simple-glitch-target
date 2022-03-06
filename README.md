# ChipWhisperer Simple Serial Glitch Target

This is a collection of the files used for the [ChipWhisperer Glitch Tutorial](https://chipwhisperer.readthedocs.io/en/latest/tutorials/courses_fault101_soln_fault%201_1%20-openadc-cwlitearm.html).

## SimpleSerial Protocol and ChipWhisperer

More info on the SimpleSerial V2 protocol can be found
[here](https://github.com/newaetech/chipwhisperer/blob/develop/hardware/victims/firmware/simpleserial/README.md).

More info on the ChipWhisperer framework can be found
[here](https://github.com/newaetech/chipwhisperer).

## Usage

> Note: when using this repository remember to pull in the submodule with 
> `git submodule update --init`.

One can adjust the `main.c` as one sees fit to implement their own algorithm.
Setting one of the platforms specified in the *PLATFORMS.md* in the *makefile*
will create the output files for that specified platform. By default it is set
to the `CWLITEARM`.

To run the _Python 3_ capturing code, we first need the newest version of the
ChipWhisperer python library. Then we can run `python3 capture_trace.py` in the
root directory.

## Debugging

It is possible to use `make debugging` to make *debug-target* executable with
which you can do some rough debugging. You can also check the `DEBUGGING`
constant if you want to add some conditional statement for debugging. For
example:

```c
#ifdef DEBUGGING
printf("I was here in debugging mode!\n");
#endif
```

## Contribution

If there are any issues or you can add a tested capture example for a different
platform, you can submit an issue or pull request.

## License

Licensed under a __MIT__ license.
