### Test Structure

```bash
tests/
    unit/
        ...
    integration/
        ...
    e2e/
        ...
```

Each folder in the test structure corresponds to a particular type of test that you can write.

The `unit/`, `integration/`, and `e2e/` folders contain tests that check different aspects of your application.

### Unit tests

Unit tests are tests that check individual components of your application, such as `models`, `forms`, `utilities`, etc.
To write tests of this type, you can create a `unit/` folder inside the `tests/` folder and create folders that
correspond to your application and its components.

### Integration tests

Integration tests are tests that check the interaction between components of your application, such as `views`
, `templates`,
`APIs`, etc. To write tests of this type, you can create an `integration/` folder inside the `tests/` folder and create
folders that correspond to your application and its components.

### E2E tests

E2E (End-to-End) tests are tests that check the interaction between the user and your application, including input and
output data. To write tests of this type, you can create an `e2e/` folder inside the `tests/` folder and create folders
that correspond to your application and its components.