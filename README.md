# TypstList

Simple script to compile as many typst files as there are row in a specified table. The table file can be a csv or .xlsx, .xls, .json, .html or .parquet file. The table file must have a header row with the keys of each values. The key=value are passed to the sys.inputs of the Typst compiler.  See [sys.inputs](https://typst.app/docs/reference/foundations/sys).

## Dependencies

[Typst](https://typst.app/#start) comptiler must be installed on your system. You can find how to install it [here](https://github.com/typst/typst).

Dependencies are managed by [UV](https://docs.astral.sh/uv/).
```bash
uv sync
```

## To do
- [x] name default newly created folder after the name of the .typ file.
- [x] add an option to specify which key tu use to name each file compiled. If not specified, use the name of the ".typ" file.
- [x] escape all character in values.
- [x] read from multiple table file type.
- [x] read from a specific sheet of a excel file.
- [ ] add global sys input by CLI option. Example for date time.
- [ ] make equation in $$ available to the compiler.
- [ ] add example.

