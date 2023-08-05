Changes
=======

Unreleased
----------

* Document changes here, in categories: Interface changes, Documentation
  changes, Code changes.  Use ``~~~`` to underline the headings, and do
  not leave a blank line between the heading and the first list item.

0.2.0 (2019-04-22)
------------------

Interface changes
~~~~~~~~~~~~~~~~~
* On startup, files are now uploaded in order of mtime instead of in
  alphabetical order.  This cannot be precise, so the actual order
  should be considered arbitrary (a change from version 0.1.1), but it
  is still the most intuitive behaviour.

0.1.1 (2019-04-21)
------------------

Interface changes
~~~~~~~~~~~~~~~~~
* On startup, files are now uploaded in alphabetical order instead of in
  arbitrary (filesystem) order.  This is helpful if the files are
  timestamped in some way and does not hurt otherwise.

0.1.0 (2019-04-21)
------------------

* Initial release.
