# Copyright (C) 2022 Matt Langston. All Rights Reserved.
load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_addendum_1",
    srcs = [
        "test_addendum_1.py",
        "test_constants.py",
        "test_dataset.py",
        "test_weighted_means.py",
    ],
    data = [
        "//data:csv_files",
    ],
    main = "test_addendum_1.py",
    deps = [
        "//fractal_governance",
    ],
)
