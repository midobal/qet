# Quality Estimation Tagger #

This software generates word-level/phrase-level QE tags for a given translated text and its post-edited version. Following the *WMT shared task*'s notation, correct words/phrases are tagged as **OK**, and errors are tagged as **BAD**.

## Dependencies ##

The **phrase-level** tagger makes use of [mgiza](https://github.com/moses-smt/mgiza).

## Usage ##

```bash
QET.py -t translation_file -pe post-edited_file {-p source_file mgiza_path}
```

Where:

  * **translation_file** is the translated text.
  * **post-edited_file** is the post-edited version of the translated text.
  * **-p** switches to phrase-level generation.
  * **source_file** is the original text.
  * **mgiza_path** is the path to mgiza's bin folder (e.g., */opt/mgiza/mgizapp/bin/*).

## Examples ##

### Word-level QE ###

**Source:** El profundo mar azul .

**Translation:** The deep sea blue .

**Post-edited:** The deep blue sea .

**Tags:** OK OK BAD OK OK

### Phrase-level QE ###

**Source:** El profundo mar azul .

**Translation:** The deep sea blue .

**Post-edited:** The deep blue sea .

**Tags:** OK BAD BAD OK OK

