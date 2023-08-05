# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module to manage all the Dataset enums."""

from enum import Enum


class HistogramCompareMethod(Enum):
    """Select the metric used to measure the difference between distributions of numeric columns in two profiles."""

    WASSERSTEIN = 0  #: Selects `Wasserstein metric <https://wikipedia.org/wiki/Wasserstein_metric>`_
    ENERGY = 1  #: Selects `Energy distance <https://wikipedia.org/wiki/Energy_distance>`_


class PromoteHeadersBehavior(Enum):
    """Control how column headers are read from files."""

    NoHeaders = 0  #: No column headers are read
    OnlyFirstFileHasHeaders = 1  #: Read headers only from first row of first file, everything else is data.
    CombineAllFilesHeaders = 2  #: Read headers from first row of each file, combining identically named columns.
    AllFilesHaveSameHeaders = 3  #: Read headers from first row of first file, drops first row from other files.


class SkipLinesBehavior(Enum):
    """Control how leading rows are skipped from files."""

    NoRows = 0  #: All rows from all files are read, none are skipped.
    FromFirstFileOnly = 1  #: Skip rows from  first file, reads all rows from other files.
    FromAllFiles = 2  #: Skip rows from each file.


class FileEncoding(Enum):
    """File encoding options."""

    UTF8 = 0
    ISO88591 = 1
    LATIN1 = 2
    ASCII = 3
    UTF16 = 4
    UTF32 = 5
    UTF8BOM = 6
    WINDOWS1252 = 7


class FileType(Enum):
    """class of the representation of a FileTypes."""

    Csv = "Csv"
    Tsv = "Tsv"
    Txt = "Txt"
    Json = "Json"
    Excel = "Excel"
    Parquet = "Parquet"
    Binary = "Binary"
    Zip = "Zip"
    Unknown = "Unknown"
