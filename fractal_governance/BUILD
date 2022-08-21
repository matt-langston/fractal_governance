# Copyright (C) 2022 Matt Langston. All Rights Reserved.
load("@rules_python//python:defs.bzl", "py_library")
load("@python_dependencies//:requirements.bzl", "requirement")

py_library(
    name = "fractal_governance",
    srcs = [
        "__init__.py",
        "addendum_1/constants.py",
        "addendum_1/dataset.py",
        "addendum_1/token_supply.py",
        "addendum_1/weighted_means.py",
        "constants.py",
        "dataset.py",
        "math.py",
        "plots.py",
        "statistics.py",
        "util.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        requirement("attrs"),
        requirement("matplotlib"),
        requirement("numpy"),
        requirement("pandas"),
        requirement("scipy"),
        requirement("streamlit"),
        requirement("uncertainties"),
    ],
)
