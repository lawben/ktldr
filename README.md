# kTLDR

kTLDR is a small script to extract your highlights from your Kindle.

### Usage:
```sh
> python3 ktldr.py /path/to/kindle /path/to/output_dir
```
The output directory must exist already.

### Example:
```sh
> cat kindle-clipping-file
On Liberty (John Stuart Mill)
- Your Highlight at location 411-412 | Added on Thursday, 28 June 2018 14:29:13

The only freedom which deserves the name, is that of pursuing our own good in our own way, so long as we do not attempt to deprive others of theirs, or impede their efforts to obtain it.
==========
Deep Work (Cal Newport)
- Your Highlight at location 1519-1520 | Added on Friday, 13 April 2018 12:04:15

Discipline #1: Focus on the Wildly Important
==========

> python3 ktldr.py /Volume/Kindle ~/my-tldrs   # /Volumes/Kindle is the default on OSX

> ls ~/my-tldrs
Deep_Work_(Cal_Newport)-TLDR.md
On_Liberty_(John_Stuart_Mill)-TLDR.md

> cat ~/my-tldrs/Deep_Work_\(Cal_Newport\)-TLDR.md
# TLDR for Deep Work (Cal Newport)
- Discipline #1: Focus on the Wildly Important
```

### Add to .bashrc/.zshrc:
For convenience, you can add this to you .zshrc because the location of the Kindle and of the TLDRs will probably always be the same.

```sh
alias ktldr='python3 ~/repos/ktldr/ktldr.py /Volumes/Kindle ~/my-tldrs'
```
