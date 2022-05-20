# Copyright (C) 2022 Matt Langston. All Rights Reserved.
load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_fractal_governance",
    srcs = [
        "test_dataset.py",
        "test_fractal_governance.py",
        "test_math.py",
        "test_plots.py",
        "test_statistics.py",
        "test_util.py",
    ],
    data = [
        "//data:csv_files",
    ],
    main = "test_fractal_governance.py",
    deps = [
        "//fractal_governance",
    ],
)
