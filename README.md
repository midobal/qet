# Quality Estimation Tagger #

This software generates word-level/phrase-level QE tags for a given translated text and its post-edited version. Following the *WMT shared task*'s notation, correct words/phrases are tagged as **OK**, and errors are tagged as **BAD**.

## Usage ##

```bash
QET.py -t translation_file -pe post-edited_file {-p}
```

Where:

  * **translation_file** is the translated text.
  * **post-edited_file** is the post-edited version of the translated text.
  * **-p** switches to phrase-level generation.

## Examples ##

### Word-level QE ###

**Source:** El profundo mar azul .

**Translation:** The deep sea blue .

**Post-edited:** The deep blue sea .

**Tags:** OK OK BAD BAD OK

