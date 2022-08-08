# Copyright (C) 2022 Matt Langston. All Rights Reserved.
load("@rules_python//python:defs.bzl", "py_library")
load("@python_dependencies//:requirements.bzl", "requirement")

py_library(
    name = "fractal_governance",
    srcs = [
        "__init__.py",
        "dataset.py",
        "math.py",
        "plots.py",
        "statistics.py",
        "token_supply.py",
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
