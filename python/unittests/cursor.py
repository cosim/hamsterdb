#
# Copyright (C) 2005-2015 Christoph Rupp (chris@crupp.de).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest

# set the library path, otherwise hamsterdb.so/.dll is not found
import os
import sys
import distutils.util
p     =  distutils.util.get_platform()
ps    =  ".%s-%s" % (p, sys.version[0:3])
sys.path.insert(0, os.path.join('build', 'lib' + ps))
sys.path.insert(1, os.path.join('..', 'build', 'lib' + ps))
import hamsterdb

class CursorTestCase(unittest.TestCase):
  def testClone(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    c = hamsterdb.cursor(db)
    clone = c.clone()
    c.close()
    clone.close()
    db.close()

  def testCloneAutoClose(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    c = hamsterdb.cursor(db)
    clone = c.clone()
    c.close()
    clone.close()
    db.close()
    env.close()

  def testCloneNegative(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    c = hamsterdb.cursor(db)
    try:
      clone = c.clone(13)
    except TypeError:
      pass
    c.close()
    db.close()
    env.close()

  def testMoveTo(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    db.insert(None, "key1", "value1")
    db.insert(None, "key2", "value2")
    db.insert(None, "key3", "value3")
    c = hamsterdb.cursor(db)
    c.move_to(hamsterdb.HAM_CURSOR_FIRST)
    c.move_to(hamsterdb.HAM_CURSOR_NEXT)
    c.move_to(hamsterdb.HAM_CURSOR_LAST)
    c.close()
    db.close()
    env.close()

  def testMoveToNegative(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    try:
      c = hamsterdb.cursor()
    except TypeError:
      pass
    try:
      c = hamsterdb.cursor("blah")
    except TypeError:
      pass
    try:
      c = hamsterdb.cursor(db)
      c.move_to(hamsterdb.HAM_CURSOR_FIRST)
    except hamsterdb.error, (errno, string):
      assert hamsterdb.HAM_KEY_NOT_FOUND  == errno
    c.close()
    db.close()
    env.close()

  def testGetKey(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    db.insert(None, "key1", "value1")
    db.insert(None, "key2", "value2")
    db.insert(None, "key3", "value3")
    c = hamsterdb.cursor(db)
    c.move_to(hamsterdb.HAM_CURSOR_FIRST)
    assert "key1"  == c.get_key()
    c.move_to(hamsterdb.HAM_CURSOR_NEXT)
    assert "key2"  == c.get_key()
    c.move_to(hamsterdb.HAM_CURSOR_LAST)
    assert "key3"  == c.get_key()
    c.close()
    db.close()
    env.close()

  def testGetKeyNegative(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    c = hamsterdb.cursor(db)
    try:
      c.get_key()
    except hamsterdb.error, (errno, string):
      assert hamsterdb.HAM_CURSOR_IS_NIL  == errno
    try:
      c.get_key(333)
    except TypeError:
      pass
    c.close()
    db.close()
    env.close()

  def testGetRecord(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    db.insert(None, "key1", "value1")
    db.insert(None, "key2", "value2")
    db.insert(None, "key3", "value3")
    c = hamsterdb.cursor(db)
    c.move_to(hamsterdb.HAM_CURSOR_FIRST)
    assert "value1"  == c.get_record()
    c.move_to(hamsterdb.HAM_CURSOR_NEXT)
    assert "value2"  == c.get_record()
    c.move_to(hamsterdb.HAM_CURSOR_LAST)
    assert "value3"  == c.get_record()
    c.close()
    db.close()
    env.close()

  def testGetRecordNegative(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    c = hamsterdb.cursor(db)
    try:
      c.get_record()
    except hamsterdb.error, (errno, string):
      assert hamsterdb.HAM_CURSOR_IS_NIL  == errno
    try:
      c.get_record(333)
    except TypeError:
      pass
    c.close()
    db.close()
    env.close()

  def testGetOverwrite(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    db.insert(None, "key1", "value1")
    db.insert(None, "key2", "value2")
    db.insert(None, "key3", "value3")
    c = hamsterdb.cursor(db)
    c.move_to(hamsterdb.HAM_CURSOR_FIRST)
    assert "value1"  == c.get_record()
    c.overwrite("value11");
    assert "value11"  == c.get_record()
    c.move_to(hamsterdb.HAM_CURSOR_NEXT)
    assert "value2"  == c.get_record()
    c.overwrite("value22");
    assert "value22"  == c.get_record()
    c.move_to(hamsterdb.HAM_CURSOR_LAST)
    assert "value3"  == c.get_record()
    c.overwrite("value33");
    assert "value33"  == c.get_record()
    c.close()
    db.close()
    env.close()

  def testGetOverwrite(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    c = hamsterdb.cursor(db)
    try:
      c.overwrite("asdf")
    except hamsterdb.error, (errno, string):
      assert hamsterdb.HAM_CURSOR_IS_NIL  == errno
    try:
      c.overwrite(None)
    except TypeError:
      pass
    try:
      c.overwrite(33)
    except TypeError:
      pass
    c.close()
    db.close()
    env.close()

  def testFind(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    db.insert(None, "key1", "value1")
    db.insert(None, "key2", "value2")
    db.insert(None, "key3", "value3")
    c = hamsterdb.cursor(db)
    c.find("key1")
    assert "key1"  == c.get_key()
    assert "value1"  == c.get_record()
    c.find("key3")
    assert "key3"  == c.get_key()
    assert "value3"  == c.get_record()
    c.find("key2")
    assert "key2"  == c.get_key()
    assert "value2"  == c.get_record()
    c.close()
    db.close()
    env.close()

  def testFindRecno(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1, hamsterdb.HAM_RECORD_NUMBER64)
    db.insert(None, 1, "value1")
    db.insert(None, 2, "value2")
    db.insert(None, 3, "value3")
    c = hamsterdb.cursor(db)
    c.find(1)
    assert 1  == c.get_key()
    assert "value1"  == c.get_record()
    try:
      c.find("1")
    except TypeError:
      pass
    c.close()
    db.close()
    env.close()

  def testFindNegative(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    db.insert(None, "key1", "value1")
    db.insert(None, "key2", "value2")
    db.insert(None, "key3", "value3")
    c = hamsterdb.cursor(db)
    try:
      c.find("key4")
    except hamsterdb.error, (errno, string):
      assert hamsterdb.HAM_KEY_NOT_FOUND  == errno
    try:
      c.find(1)
    except TypeError:
      pass
    try:
      c.find()
    except TypeError:
      pass
    c.close()
    db.close()
    env.close()

  def testInsert(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    c = hamsterdb.cursor(db)
    c.insert("key1", "value1")
    assert "key1"  == c.get_key()
    assert "value1"  == c.get_record()
    c.insert("key3", "value3")
    assert "key3"  == c.get_key()
    assert "value3"  == c.get_record()
    c.insert("key2", "value2")
    assert "key2"  == c.get_key()
    assert "value2"  == c.get_record()
    c.close()
    db.close()
    env.close()

  def testInsertRecno(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1, hamsterdb.HAM_RECORD_NUMBER32)
    c = hamsterdb.cursor(db)
    c.insert(1, "value1")
    assert 1  == c.get_key()
    assert "value1"  == c.get_record()
    c.insert(2, "value2")
    c.insert(3, "value3")
    try:
      c.insert("1", "blah")
    except TypeError:
      pass
    c.close()
    db.close()
    env.close()

  def testInsertNegative(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    c = hamsterdb.cursor(db)
    try:
      c.insert(3, "value1")
    except TypeError:
      pass
    try:
      c.insert("a", "key2", "value2")
    except TypeError:
      pass
    try:
      c.insert()
    except TypeError:
      pass
    try:
      c.insert("key1", "value1")
      c.insert("key1", "value1")
    except hamsterdb.error, (errno, string):
      assert hamsterdb.HAM_DUPLICATE_KEY  == errno
    c.close()
    db.close()
    env.close()

  def testErase(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    c = hamsterdb.cursor(db)
    c.insert("key1", "value1")
    assert "key1"  == c.get_key()
    assert "value1"  == c.get_record()
    c.erase()
    try:
      c.find("key1")
    except hamsterdb.error, (errno, string):
      assert hamsterdb.HAM_KEY_NOT_FOUND  == errno
    c.close()
    db.close()
    env.close()

  def testEraseNegative(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1)
    c = hamsterdb.cursor(db)
    try:
      c.erase(3)
    except TypeError:
      pass
    try:
      c.erase("a", "key2", "value2")
    except TypeError:
      pass
    try:
      c.erase()
    except hamsterdb.error, (errno, string):
      assert hamsterdb.HAM_CURSOR_IS_NIL  == errno
    c.close()
    db.close()
    env.close()

  def testGetDuplicateCount(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1, hamsterdb.HAM_ENABLE_DUPLICATE_KEYS)
    c = hamsterdb.cursor(db)
    c.insert("key1", "value1")
    assert 1  == c.get_duplicate_count()
    c.insert("key1", "value2", hamsterdb.HAM_DUPLICATE)
    assert 2  == c.get_duplicate_count()
    c.insert("key1", "value3", hamsterdb.HAM_DUPLICATE)
    assert 3  == c.get_duplicate_count()
    c.erase()
    c.move_to(hamsterdb.HAM_CURSOR_FIRST)
    assert 2  == c.get_duplicate_count()
    c.close()
    db.close()
    env.close()

  def testGetDuplicatePosition(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1, hamsterdb.HAM_ENABLE_DUPLICATE_KEYS)
    c = hamsterdb.cursor(db)
    c.insert("key1", "value1")
    c.insert("key1", "value2", hamsterdb.HAM_DUPLICATE)
    c.insert("key1", "value3", hamsterdb.HAM_DUPLICATE)
    c.insert("key1", "value4", hamsterdb.HAM_DUPLICATE)
    c.move_to(hamsterdb.HAM_CURSOR_FIRST)
    assert 0 == c.get_duplicate_position()
    c.move_to(hamsterdb.HAM_CURSOR_NEXT)
    assert 1 == c.get_duplicate_position()
    c.move_to(hamsterdb.HAM_CURSOR_NEXT)
    assert 2 == c.get_duplicate_position()
    c.move_to(hamsterdb.HAM_CURSOR_NEXT)
    assert 3 == c.get_duplicate_position()
    c.close()
    db.close()
    env.close()

  def testGetRecordSize(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1, hamsterdb.HAM_ENABLE_DUPLICATE_KEYS)
    c = hamsterdb.cursor(db)
    c.insert("key1", "v")
    c.insert("key2", "va")
    c.insert("key3", "val")
    c.insert("key4", "valu", hamsterdb.HAM_DUPLICATE)
    c.insert("key4", "value", hamsterdb.HAM_DUPLICATE)
    c.move_to(hamsterdb.HAM_CURSOR_FIRST)
    assert 1 == c.get_record_size()
    c.move_to(hamsterdb.HAM_CURSOR_NEXT)
    assert 2 == c.get_record_size()
    c.move_to(hamsterdb.HAM_CURSOR_NEXT)
    assert 3 == c.get_record_size()
    c.move_to(hamsterdb.HAM_CURSOR_NEXT)
    assert 4 == c.get_record_size()
    c.move_to(hamsterdb.HAM_CURSOR_NEXT)
    assert 5 == c.get_record_size()
    c.close()
    db.close()
    env.close()

  def testGetDuplicateCountNegative(self):
    env = hamsterdb.env()
    env.create("test.db")
    db = env.create_db(1, hamsterdb.HAM_ENABLE_DUPLICATE_KEYS)
    c = hamsterdb.cursor(db)
    try:
      c.get_duplicate_count()
    except hamsterdb.error, (errno, string):
      assert hamsterdb.HAM_CURSOR_IS_NIL  == errno
    c.insert("key1", "value1")
    try:
      c.get_key(333)
    except TypeError:
      pass
    try:
      c.get_key("asdf")
    except TypeError:
      pass
    c.close()
    db.close()
    env.close()

unittest.main()

