#!/usr/bin/env python3
# Hattifnatt -- Push directory to Telegram channel

from collections        import namedtuple
from hashlib            import sha256
from io                 import BufferedReader, RawIOBase
from queue              import Queue
from sys                import intern
from pathtools.patterns import match_path
from os                 import scandir
from os.path            import basename
from watchdog.events    import PatternMatchingEventHandler
from watchdog.observers import Observer

__all__ = ['push']


# Locking

try:
	from fcntl import LOCK_EX, LOCK_NB, LOCK_UN, lockf
except ImportError:
	from msvcrt import LK_NBRLCK, LK_UNLCK, locking
	def lock(file):
		pos = file.tell()
		try:
			file.seek(0)
			locking(file.fileno(), LK_NBRLCK, 1)
		finally:
			file.seek(pos)
	def unlock(file):
		pos = file.tell()
		try:
			file.seek(0)
			locking(file.fileno(), LK_UNLCK, 1)
		finally:
			file.seek(pos)
else:
	def lock(file):
		lockf(file, LOCK_EX | LOCK_NB)
	def unlock(file):
		lockf(file, LOCK_UN)

class Lock:
	__slots__ = ('file',)
	def __init__(self, file):
		self.file = file
	def __enter__(self):
		lock(self.file)
		return self.file
	def __exit__(self, exc_type, exc_value, exc_tb):
		unlock(self.file)


# Journal

File = namedtuple('File', ('id', 'digest'))

TOMBSTONE = '!'

def load(file, chat, patterns):
	file.seek(0); lines = iter(file)

	ver, oldchat = next(lines, chat.id).rstrip('\n').split(' ')
	if int(ver) != 1:
		raise RuntimeError("Version mismatch")
	if oldchat != str(chat.id):
		raise RuntimeError('Chat ID mismatch')

	files = dict()
	for line in lines:
		msgid, digest, name = line.rstrip('\n').split('\t', maxsplit=2)
		if not match_path(name, patterns, case_sensitive=True):
			continue
		assert (msgid == TOMBSTONE) == (digest == TOMBSTONE)
		if msgid == TOMBSTONE:
			files.pop(name, None)
		else:
			files[name] = File(int(msgid), digest)
	return files

def init(file, chat):
	print(1, chat.id, file=file, flush=True)

def save(file, name, data):
	assert '\n' not in name
	print(data.id     if data is not None else TOMBSTONE,
	      data.digest if data is not None else TOMBSTONE,
	      name,
	      sep='\t', file=file, flush=True)


# Digest

class DigestReader(RawIOBase):
	__slots__ = ('raw', '_digest')
	def __init__(self, raw):
		self.raw = raw
		self._digest = sha256() # FIXME

	def readinto(self, buffer):
		length = self.raw.readinto(buffer)
		if length is not None:
			self._digest.update(buffer[0:length])
		return length

	def digest(self):
		return self._digest.digest()

	def hexdigest(self):
		return self._digest.hexdigest()

	def close(self):
		return self.raw.close()
	@property
	def closed(self):
		return self.raw.closed
	def fileno(self):
		return self.raw.fileno()
	def flush(self):
		pass
	def isatty(self):
		return self.raw.isatty()
	def readable(self):
		return self.raw.readable()

def readdigest(name):
	try:
		file = DigestReader(open(name, 'rb', buffering=0))
	except OSError:
		return None
	with file:
		while file.read():
			pass
		return file.hexdigest()


# Telegram

def create(chat, name):
	try:
		dig = DigestReader(open(name, 'rb', buffering=0))
	except OSError:
		print('zombie {}'.format(name), flush=True)
		return
	with BufferedReader(dig) as buf:
		print('create {}'.format(name), flush=True)
		msg  = chat.send_document(buf, filename=name)
		file = File(msg.message_id, dig.hexdigest())
		print('upload {} ({}, {})'.format(name, file.id, file.digest),
		      flush=True)
		return file

def delete(chat, name, file):
	print('delete {} ({}, {})'.format(name, file.id, file.digest),
	      flush=True)
	chat.bot.delete_message(chat.id, file.id)


# Events

CREATE = intern('create')
DELETE = intern('delete')

class Handler(PatternMatchingEventHandler):
	def __init__(self, queue, *args, **named):
		named.setdefault('ignore_directories', True)
		named.setdefault('case_sensitive', True)
		super().__init__(*args, **named)
		self._queue = queue

	def on_created(self, event):
		self._queue.put((CREATE, event.src_path))
	def on_deleted(self, event):
		self._queue.put((DELETE, event.src_path))
	def on_modified(self, event):
		self._queue.put((DELETE, event.src_path))
		self._queue.put((CREATE, event.src_path))
	def on_moved(self, event):
		self._queue.put((DELETE, event.src_path))
		self._queue.put((CREATE, event.dest_path))


# Main loop

JOURNAL = '.hat'

def push(chat, patterns):
	with Lock(open(JOURNAL, 'a+')) as journal:
		if journal.tell() == 0:
			init(journal, chat)
		files = load(journal, chat, patterns)

		queue = Queue()
		handler = Handler(queue, patterns)
		observer = Observer()

		observer.schedule(handler, '.', recursive=False)
		try:
			observer.start()

			actual = dict()
			for entry in scandir():
				if (not entry.is_file() or
				    not match_path(entry.name, patterns,
				                   case_sensitive=True) or
				    entry.name == JOURNAL):
					continue
				actual[entry.name] = readdigest(entry.name)

			oldnames = set(files.keys())
			newnames = set(actual.keys())
			new = newnames - oldnames
			old = oldnames - newnames
			for name in oldnames & newnames:
				if files[name].digest != actual[name]:
					old.add(name)
					new.add(name)

			while True:
				if old:
					type, name = DELETE, old.pop()
				elif new:
					type, name = CREATE, new.pop()
				else:
					type, name = queue.get()
				name = basename(name)

				if name == JOURNAL:
					continue
				if name in files:
					save(journal, name, None)
					delete(chat, name, files[name])
					del files[name]
				if type is CREATE:
					file = create(chat, name)
					save(journal, name, file)
					if file is not None:
						files[name] = file
		except KeyboardInterrupt:
			pass
		finally:
			observer.stop()

		observer.join()


# Command-line tool

def main():
	from os       import environ
	from sys      import argv, exit, stderr
	from telegram import Bot

	TOKEN = environ.get('TOKEN', '')
	CHAT  = environ.get('CHAT', '')
	# PTB sets HTTPS proxy from environ['HTTPS_PROXY']
	patterns = argv[1:] if len(argv) > 1 else ['*']

	if not TOKEN:
		print('error: no bot token in environment', file=stderr)
		exit(1)
	if not CHAT:
		print('error: no chat id in environment', file=stderr)
		exit(1)

	push(Bot(token=TOKEN).get_chat(CHAT), patterns)

if __name__ == '__main__':
	main()
