```
This module is intended to provide configuration functionality for Python
programs.

Change History
--------------

Version   Date        Description
=============================================================================
0.4.1     30 Apr 2019 Fixed bug in stream handling. Thanks to Kathryn Mazaitis
                      for the report and patch. Updated trove classifiers.
-----------------------------------------------------------------------------
0.4.0     07 Dec 2016 Made minor changes to allow tests to pass in Python 3.
                      Support for Python < 2.6 has been dropped.
                      Updated trove classifiers and other information which
                      feeds into PKG-INFO. Used more standardised wording
                      for the licence (3-clause BSD).
-----------------------------------------------------------------------------
0.3.9     11 May 2010 Fixed parsing bug which caused failure for numbers with
                      exponents.
-----------------------------------------------------------------------------
0.3.8     03 Mar 2010 Fixed parsing bug which caused failure for negative
                      numbers in sequences. Improved resolution logic.
-----------------------------------------------------------------------------
0.3.7     05 Oct 2007 Added Mapping.__delitem__ (patch by John Drummond).
                      Mapping.__getattribute__ no longer returns "" when
                      asked for "__class__" - doing so causes pickle to
                      crash (reported by Jamila Gunawardena).
                      Allow negative numbers (reported by Gary Schoep; had
                      already been fixed but not yet released).
-----------------------------------------------------------------------------
0.3.6     09 Mar 2006 Made classes derive from object (previously they were
                      old-style classes).
                      Changed ConfigMerger to use a more flexible merge
                      strategy.
                      Multiline strings (using """ or ''') are now supported.
                      A typo involving raising a ConfigError was fixed.
                      Patches received with thanks from David Janes & Tim
                      Desjardins (BlogMatrix) and Erick Tryzelaar.
-----------------------------------------------------------------------------
0.3.5     27 Dec 2004 Added ConfigOutputStream to provide better Unicode
                      output support. Altered save code to put platform-
                      dependent newlines for Unicode.
-----------------------------------------------------------------------------
0.3.4     11 Nov 2004 Added ConfigInputStream to provide better Unicode
                      support.
                      Added ConfigReader.setStream().
-----------------------------------------------------------------------------
0.3.3     09 Nov 2004 Renamed config.get() to getByPath(), and likewise for
                      ConfigList.
                      Added Mapping.get() to work like dict.get().
                      Added logconfig.py and logconfig.cfg to distribution.
-----------------------------------------------------------------------------
0.3.2     04 Nov 2004 Simplified parseMapping().
                      Allowed Config.__init__ to accept a string as well as a
                      stream. If a string is passed in, streamOpener is used
                      to obtain the stream to be used.
-----------------------------------------------------------------------------
0.3.1     04 Nov 2004 Changed addNamespace/removeNamespace to make name
                      specification easier.
                      Refactored save(), added Container.writeToStream and
                      Container.writeValue() to help with this.
-----------------------------------------------------------------------------
0.3       03 Nov 2004 Added test harness (test_config.py)
                      Fixed bugs in bracket parsing.
                      Refactored internal classes.
                      Added merging functionality.
-----------------------------------------------------------------------------
0.2       01 Nov 2004 Added support for None.
                      Stream closed in load() and save().
                      Added support for changing configuration.
                      Fixed bugs in identifier parsing and isword().
-----------------------------------------------------------------------------
0.1       31 Oct 2004 Initial implementation (for community feedback)
-----------------------------------------------------------------------------

-----------------------------------------------------------------------------
COPYRIGHT
-----------------------------------------------------------------------------
Copyright (C) 2004-2016 by Vinay Sajip. All Rights Reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
