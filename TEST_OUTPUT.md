Found 6 test(s).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, sitemaps
  Apply all migrations: admin, auth, contenttypes, packaging, sessions
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying packaging.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying sessions.0001_initial... OK
System check identified no issues (0 silenced).
test_recommend_box_api_malformed_json (packaging.tests.BoxSelectionAPITests.test_recommend_box_api_malformed_json) ... ok
test_recommend_box_api_success (packaging.tests.BoxSelectionAPITests.test_recommend_box_api_success) ... ok
test_3d_rotation_fit (packaging.tests.BoxSelectionLogicTests.test_3d_rotation_fit) ... ok
test_invalid_negative_dimensions (packaging.tests.BoxSelectionLogicTests.test_invalid_negative_dimensions) ... ok
test_item_exceeds_all_box_dimensions (packaging.tests.BoxSelectionLogicTests.test_item_exceeds_all_box_dimensions) ... ok
test_weight_limit_triggers_box_upgrade (packaging.tests.BoxSelectionLogicTests.test_weight_limit_triggers_box_upgrade) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.024s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...