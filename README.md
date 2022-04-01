# ChipWhisperer Simple Serial Glitch Target

This is a collection of the files used for the [ChipWhisperer Glitch Tutorial](https://chipwhisperer.readthedocs.io/en/latest/tutorials/courses_fault101_soln_fault%201_1%20-openadc-cwlitearm.html).

## Requirements

- [ARM GNU Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm). Can be installed using your favourite package manager (often under the name `arm-none-eabi-gcc`).
- MatplotLib. Installed with `pip3 install matplotlib`
- NumPy. Installed with `pip3 install numpy`
- Struct. Installed with `pip3 install struct`
- TQDM. Installed with `pip3 install tqdm`

## Usage

> Note: when using this repository remember to pull in the submodule with 
> `git submodule update --init`.

If you just want to see the result for yourself, connect your CW-Lite ARM and
run the following commands.
```bash
make
python3 clock_glitch.py
```

## License

Licensed under a __MIT__ license.
