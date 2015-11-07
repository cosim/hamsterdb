/*
 * Copyright (C) 2005-2015 Christoph Rupp (chris@crupp.de).
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 * A Cursor is an object which is used to traverse a Database.
 *
 * A Cursor structure is separated into 3 components:
 * 1. The btree cursor
 *      This cursor can traverse btrees. It is described and implemented
 *      in btree_cursor.h.
 * 2. The txn cursor
 *      This cursor can traverse txn-trees. It is described and implemented
 *      in txn_cursor.h.
 * 3. The upper layer
 *      This layer acts as a kind of dispatcher for both cursors. If
 *      Transactions are used, then it also uses a duplicate cache for
 *      consolidating the duplicate keys from both cursors. This layer is
 *      described and implemented in cursor.h (this file).
 *
 * A Cursor can have several states. It can be
 * 1. NIL (not in list) - this is the default state, meaning that the Cursor
 *      does not point to any key. If the Cursor was initialized, then it's
 *      "NIL". If the Cursor was erased (i.e. with ham_cursor_erase) then it's
 *      also "NIL".
 *
 *      relevant functions:
 *          Cursor::is_nil
 *          Cursor::set_to_nil
 *
 * 2. Coupled to the txn-cursor - meaning that the Cursor points to a key
 *      that is modified in a Transaction. Technically, the txn-cursor points
 *      to a TransactionOperation structure.
 *
 *      relevant functions:
 *          Cursor::is_coupled_to_txnop
 *          Cursor::couple_to_txnop
 *
 * 3. Coupled to the btree-cursor - meaning that the Cursor points to a key
 *      that is stored in a Btree. A Btree cursor itself can then be coupled
 *      (it directly points to a page in the cache) or uncoupled, meaning that
 *      the page was purged from the cache and has to be fetched from disk when
 *      the Cursor is used again. This is described in btree_cursor.h.
 *
 *      relevant functions:
 *          Cursor::is_coupled_to_btree
 *          Cursor::couple_to_btree
 *
 * The dupecache is used when information from the btree and the txn-tree
 * is merged. The btree cursor has its private dupecache. The dupecache
 * increases performance (and complexity).
 *
 * The cursor interface is used in db_local.cc. Many of the functions use
 * a high-level cursor interface (i.e. @ref cursor_create, @ref cursor_clone)
 * while some directly use the low-level interfaces of btree_cursor.h and
 * txn_cursor.h. Over time i will clean this up, trying to maintain a clear
 * separation of the 3 layers, and only accessing the top-level layer in
 * cursor.h. This is work in progress.
 *
 * In order to speed up Cursor::move() we keep track of the last compare
 * between the two cursors. i.e. if the btree cursor is currently pointing to
 * a larger key than the txn-cursor, the 'lastcmp' field is <0 etc.
 *
 * @exception_safe: unknown
 * @thread_safe: unknown
 */

#ifndef HAM_CURSOR_H
#define HAM_CURSOR_H

#include "0root/root.h"

// Always verify that a file of level N does not include headers > N!
#include "1base/error.h"

#ifndef HAM_ROOT_H
#  error "root.h was not included"
#endif

// A helper structure; ham_cursor_t is declared in ham/hamsterdb.h as an
// opaque C structure, but internally we use a C++ class. The ham_cursor_t
// struct satisfies the C compiler, and internally we just cast the pointers.
struct ham_cursor_t
{
  bool _dummy;
};

namespace hamsterdb {

class Database;
class LocalDatabase;
class Transaction;

//
// the Database Cursor
//
class Cursor
{
  public:
    // Constructor; retrieves pointer to db and txn, initializes all members
    Cursor(Database *db, Transaction *txn = 0)
      : m_db(db), m_txn(txn), m_next(0), m_previous(0) {
    }

    // Copy constructor; used for cloning a Cursor
    Cursor(Cursor &other)
      : m_db(other.m_db), m_txn(other.m_txn), m_next(0), m_previous(0) {
    }

    // Destructor
    virtual ~Cursor() {
    }

    // Returns the Database that this cursor is operating on
    Database *db() {
      return (m_db);
    }

    // Returns the Transaction handle
    Transaction *get_txn() {
      return (m_txn);
    }

    // Get the 'next' Cursor in this Database
    Cursor *get_next() {
      return (m_next);
    }

    // Set the 'next' Cursor in this Database
    void set_next(Cursor *next) {
      m_next = next;
    }

    // Get the 'previous' Cursor in this Database
    Cursor *get_previous() {
      return (m_previous);
    }

    // Set the 'previous' Cursor in this Database
    void set_previous(Cursor *previous) {
      m_previous = previous;
    }

    // Overwrites the record of a cursor (ham_cursor_overwrite)
    ham_status_t overwrite(ham_record_t *record, uint32_t flags);

    // Returns position in duplicate list (ham_cursor_get_duplicate_position)
    ham_status_t get_duplicate_position(uint32_t *pposition);

    // Returns number of duplicates (ham_cursor_get_duplicate_count)
    ham_status_t get_duplicate_count(uint32_t flags, uint32_t *pcount);

    // Get current record size (ham_cursor_get_record_size)
    ham_status_t get_record_size(uint64_t *psize);

    // Closes the cursor
    virtual void close() = 0;

  protected:
    friend struct TxnCursorFixture;

    // The Database that this cursor operates on
    Database *m_db;

    // Pointer to the Transaction
    Transaction *m_txn;

    // Linked list of all Cursors in this Database
    Cursor *m_next, *m_previous;

  private:
    // Implementation of overwrite()
    virtual ham_status_t do_overwrite(ham_record_t *record, uint32_t flags) = 0;

    // Implementation of get_duplicate_position()
    virtual ham_status_t do_get_duplicate_position(uint32_t *pposition) = 0;

    // Returns number of duplicates (ham_cursor_get_duplicate_count)
    virtual ham_status_t do_get_duplicate_count(uint32_t flags,
                        uint32_t *pcount) = 0;

    // Get current record size (ham_cursor_get_record_size)
    virtual ham_status_t do_get_record_size(uint64_t *psize) = 0;
};

} // namespace hamsterdb

#endif /* HAM_CURSOR_H */
