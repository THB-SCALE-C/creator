Template zips must have the same top-level layout as `default.zip`. The unit_assembler expects the `jinja/` templates and the `unit/` H5P package tree at the root of the archive.

Required structure (root of the zip):

```
jinja/
  main.j2
  slide.j2
  elements/
    *.j2
unit/
  content/
    content.json
  <H5P library folders and assets...>
```

Must contain:
    - `jinja/` contains the Jinja templates the assembler renders (`main.j2` + `slide.j2` + element templates).
    - `unit/` is the H5P content bundle; include `content/content.json` and all library folders/assets referenced by that content.
    - `valid.py` is present in `default.zip`; include it if you want the same validation hook.

Note:
`main.j2`serves as the entry point for the content json and should route to all sub-templates automatically.