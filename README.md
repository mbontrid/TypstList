# TypstList

Take the keys of a table and compile as many typst documents as there are rows. These key=value are made available to the compiler as sys.inputs. See [sys.inputs](https://typst.app/docs/reference/foundations/sys).


## Dependencies

[Typst](https://typst.app/#start) comptiler must be installed on your system. You can find how to do it [here](https://github.com/typst/typst).

## To do
- [x] name default newly created folder after the name of the .typ file.
- [x] add an option to specify which key tu use to name each file compiled. If not specified, use the name of the ".typ" file.
- [x] escape all character in values.
- [x] read from multiple table file type.
- [ ] add global sys input by CLI option. Example for date time.
- [ ] make equation in $$ available to the compiler.

