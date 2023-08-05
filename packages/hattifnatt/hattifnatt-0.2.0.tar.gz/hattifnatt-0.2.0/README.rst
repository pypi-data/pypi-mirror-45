Push directory to Telegram channel
==================================

Hattifnatt watches a directory for changes and creates, updates or
deletes files in a Telegram channel accordingly.  File digests and
message IDs are persisted in a state file (named ``.hat``), so even
updates that occur when the watcher is not running will be pushed
correctly.  Note that Telegram will sometimes corrupt the file names on
upload; this will not break anything, but cannot be fixed by this tool,
either.  Any Telegram chat could theoretically be used---not necessarily
a channel---but the bot API limits deletion of old messages in personal
chats.

A single command-line tool is provided, ``hat``, that watches the
current directory, reads the Telegram bot token from the environment
variable TOKEN, the Telegram chat ID from the environment variable CHAT,
and the glob patterns to watch from the command-line arguments (all
files are watched by default).  The tool can be stopped by ^C.

Alternatively, the function ``hattifnatt.push(chat, patterns)`` performs
the same function programmatically.  It accepts ``chat``, a
``telegram.Chat`` object (obtained from ``telegram.Bot.get_chat``), and
a list of glob patterns.  For now it does not support pushing
directories other than the current one.
