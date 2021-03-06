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

#include "0root/root.h"

// Always verify that a file of level N does not include headers > N!
#include "4cursor/cursor.h"

#ifndef HAM_ROOT_H
#  error "root.h was not included"
#endif

namespace hamsterdb {

ham_status_t
Cursor::overwrite(ham_record_t *record, uint32_t flags)
{
  try {
    return (do_overwrite(record, flags));
  }
  catch (Exception &ex) {
    return (ex.code);
  }
}

ham_status_t
Cursor::get_duplicate_position(uint32_t *pposition)
{
  try {
    return (do_get_duplicate_position(pposition));
  }
  catch (Exception &ex) {
    *pposition = 0;
    return (ex.code);
  }
}

ham_status_t
Cursor::get_duplicate_count(uint32_t flags, uint32_t *pcount)
{
  try {
    return (do_get_duplicate_count(flags, pcount));
  }
  catch (Exception &ex) {
    *pcount = 0;
    return (ex.code);
  }
}

ham_status_t
Cursor::get_record_size(uint64_t *psize)
{
  try {
    return (do_get_record_size(psize));
  }
  catch (Exception &ex) {
    return (ex.code);
  }
}


} // namespace hamsterdb
